############################################################################
# This module is a part of the polyrot numerical package. polyrot computes 
# polytropic models of rapidly rotating planets and stars
#
# Copyright (C) 2023 Janosz Dewberry
#
# polyrot is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation, version 3.
#
# polyrot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
# Module: star
# Brief: main class for user-manipulation of stellar/planetary model
############################################################################

import numpy as np
from scipy.optimize import brentq
from scipy.special import legendre as Pn
from .helpers import terp

__all__ = ['polyStar']

class polyStar:    
    '''
        Client (borderline god) class for user manipulation of the 
        polytropic model. Constructs or loads a stellar model based on 
        user input, and provides access to model characteristics and 
        plotting capabilities.
    '''

    # methods for pseudospectral init/operations:
    from .pseudo import setGrid,setMats,set2Dops,gridToCoeff,coeffToGrid

    # methods required to initialize rotational potential
    from .rotpot import setPhiRot

    # method for generating IC's (from 1D nonrotating problem)
    from .poly1d import computeICs

    # methods for Newton-Kantorovich iteration:
    from .newton import newtonIter,updateJacobian,updateResidual

    # methods for plotting:
    from .pltstr import plotPolyStar

    def __init__(self,n,Nr,No,Nm,Om,dO=None,Phr=None,dPh=None,Ni=200,
        verbose=True,tol=1e-15,plot=True):

        # set attributes for client instance:
        self.n  = n       # float: polytropic index
        self.Nr = Nr      # int: num of interior radial grid pts
        self.No = No      # int: num of exterior radial grid pts
        self.Nm = Nm      # int: num of latitudinal grid pts 
        self.Ni = Ni      # int: num of pts used to integrate rot. pot.
        self.Om = Om      # float or fun: ang. vel. in units w/Hc=Req=1
        self.dO = dO      # fun: optional dOmega/dR 
        self.Phr= Phr     # fun: optional rot. pot. Phi_rot
        self.dPh= dPh     # fun: optional rot. pot. dPhi_rot/dR
        self.vrb= verbose # bool: set to False for quite mode
        self.tol= tol     # tolerance for change in Newton correction

        if self.vrb:
            print('')
            print('###########################################################')
            print('################## Initializing new model #################')
            print('###########################################################')
            print('')

        # set grids and spectral matrices:
        self.setGrid()
        self.setMats()
        self.set2Dops()

        # set/compute effective rotational potential:
        self.setPhiRot()

        # compute initial conditions from non-rotating problem:
        self.computeICs()

        if Om!=0:
            # Newton-iterate to find rotating solution:
            self.newtonIter()

        # compute physically relevant quantities
        self.computePhys()

        # plot model, if desired:
        if plot: 
            self.plotPolyStar()

############################################################################
################# class methods related to physical qties ##################
############################################################################

    def computePhys(self):
        '''
            Calculates relevant physical quantities (in units normalized 
            by the equatorial radius and central enthalpy). 
            Key physical variables computed:
                > rho   density 
                > pp    pressure
                > phi   gravitational potential
                > gg    (radial part of) effective gravity (grad pp)/rho 
                > rs    surface radius r_s(mu=cos theta)
                > Rp    polar radius (relative to equatorial radius)
                > lm    "eigenvalue" resulting from spatial rescaling (Boyd 2011)
                > M     total mass
                > J     total angular momentum
                > T     total kinetic energy
                > W     total gravitational energy
                > U     total internal energy
                > I     moment of inertia
                > V     Virial 2*T + U + W
                > Verr  Virial "error" 1 + (2*T + U)/W 
                > Oc    equatorial rotation rate relative to mass-shedding limit
                > Od    rotation rate relative to dynamical frequency 

        '''
        # radial and mu-derivatives:
        self.dth = self.dr[1].dot(self.dm[0].dot(self.cf.T).T)
        self.dthm= self.dm[1].dot(self.cf.T).T

        # compute density, pressure, grav. potential, and gravity from Theta:
        dev = self.th[:self.Nr] - self.Phr.reshape([self.Nr,self.Nm])
        self.rho= np.maximum(dev,0)**self.n # density
        self.pp = self.rho**(1+1./self.n)/(self.n+1) # pressure
        self.phi= self.th[-1,0] - self.th # grav. potential
        self.gg =-self.dth # (radial cpt of) effective gravity grad P/rho

        # compute surface radius by finding, at each ray of cst mu, the 
        # radius where theta<Phi_rot:
        if np.all(self.Om==0):
            self.rs = np.array([1. for i in range(self.Nm)])
        else:
            def zfun(j):
                return brentq(f=lambda x: terp(self.ri,dev[:,j],x),a=0.01,b=1.)
            try:
                self.rs = [zfun(j) for j in range(1,self.Nm)]
                self.rs = np.append([1.],self.rs)
            except:
                print('WARNING: interpolation of surface radius failed')
                self.rs = np.array([np.inf for _ in range(self.Nm)])
        self.Rp = terp(self.mu,self.rs,1.)

        # compute total mass:
        self.M = np.sum(self.rho*self.ww)

        # total AM:
        self.J = np.sum((self.rho*self.Om*(self.R[:self.Nr])**2)*self.ww)

        # moment of inertia:
        self.I = np.sum(self.ww*(self.R**2)[:self.Nr]*self.rho[:self.Nr])

        # Virial cpts, Virial, and Virial error:
        self.T = np.sum(0.5*(self.rho*self.Om**2*(self.R[:self.Nr])**2)*self.ww)
        self.U = np.sum(3*self.pp*self.ww)
        self.W = np.sum(0.5*(self.phi[:self.Nr]*self.rho)*self.ww)
        self.V = 2*self.T + self.U + self.W
        self.Verr = 1. + (2*self.T + self.U)/self.W

        # compute equatorial rotation rate relative to mass-shedding limit:
        self.Oc = self.Om[-1,0]/np.sqrt(self.gg[self.Nr-1,0])
        if self.Oc>1.:
            print('WARNING: rotation rate has surpassed the mass-shedding limit')
        
        # compute rotation rate relative to dynamical freq.:
        self.Od= self.Om*np.sqrt(4*np.pi/self.lm/self.lm/self.M)

        # print relevant data:
        if self.vrb:
            print('')
            print('###########################################################')
            print('###################### Model Summary ######################')
            print('###########################################################')
            print('')
            print(f'lam={self.lm:.6f}')
            print(f'Om(R_eq)/sqrt[G*M/R_eq^3]={self.Od[-1,0]:.6f}')
            print(f'Om(R_eq)/[(1/r)dPhi/dr|_Req]={self.Oc:.6f}')
            print(f'R_pol/R_eq={self.Rp:.6f}')
            print(f'2*T={2*self.T:.5f}, U={self.U:.5f}, W={self.W:.5f}, J={self.J:.5f}')
            print(f'T/|W|={self.T/abs(self.W):.6f}')
            print(f'Virial error = 1+(2*T+U)/W = {self.Verr:.5e}') 
        return 


    def J2n(self,n):
        '''
            Computes grav. moment J_n = int_V r^n*P_n(mu)*rho dV directly
        '''
        II = self.rho*(self.ri**(2*n))[:,None]*(Pn(2*n)(self.mu))[None,:]
        return -np.sum(II*self.ww)/self.M

    def J2nspec(self,nmx=20):
        '''
            Computes array of J_2n values using the spectral expansion 
            of the grav. potential, rather than the numerical quadrature 
            employed by J2n
        '''
        # spectral coefficients in expansion of exterior grav. field:
        GM = self.M*self.lm**2/4./np.pi
        phl= self.dmi.dot(self.phi[self.Nr:].T)/GM
        ns = np.arange(0,nmx+1,2)
        return np.array([(self.ro**(n+1)*phl[i])[0] for i,n in enumerate(ns)])