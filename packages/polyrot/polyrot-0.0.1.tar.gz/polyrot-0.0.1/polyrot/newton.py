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
# Module: newton
# Brief: subroutines for Newton-Kantorovich iteration.
############################################################################

import numpy as np
from numpy.linalg import solve

############################################################################
################### Methods to be imported into client #####################
############################################################################

def newtonIter(self,itmax=100,alp=1.,stol=1e-6):
    '''
        Main routine for computing the equilibrium structure. Refines the 
        PDE solution gained by solving the 1D Lane-Emden equation through 
        Newton-Kantorovich iteration. 
    '''

    if self.vrb:
        print('')
        print('###########################################################')
        print('#### Starting iteration for 2D solution incl. rotation ####')
        print('###########################################################')
        print('')

    self.itr= 0
    self.dl = np.ones([self.Nf*self.Nm + 1])
    while self.itr<itmax:

        # update PDE residual:
        self.updateResidual()

        # compute errors in eigenfunction and eigenvalue:
        self.errf = np.amax(abs(self.res))  # error in eigenfunction
        self.erre = abs(self.dl[0]/self.lm) # relative change in eigenval
        if self.vrb:
            self.status = f'iter {self.itr}: lam={self.lm:.4f}, '
            self.status+= f'dlam/lam={self.erre:0.2e}, '
            self.status+= f'max[resid]={self.errf:0.2e}'
            print(self.status)

        # check for convergence:
        self.conv = min(self.erre,self.errf)
        if self.conv<=self.tol:
            print('2D iteration converged')
            break

        # update Jacobian:
        self.updateJacobian()

        # solve for correction:
        self.dl = np.append(linsolve(self.JJ[:1-self.Nm,:1-self.Nm],
                                     self.res[:1-self.Nm]),np.zeros([self.Nm-1]))
        self.lm = max(self.lm + self.dl[0]*alp,1.)
        self.cf+= self.dl[1:].reshape([self.Nf,self.Nm])*alp

        # transfer coeffs to grid-pt values:
        self.coeffToGrid()

        # update iteration state:
        self.itr+=1

    # return warning if model appears not to have converged:
    if self.conv>self.tol:
        print('WARNING: model appears not to have converged')

    # check spectral convergence:
    cmx = np.amax(abs(self.cf))
    self.chebierr = np.amax(abs(self.cf[self.Nr-1]))/cmx
    self.cheboerr = np.amax(abs(self.cf[-1]))/cmx
    self.legerr   = np.amax(abs(self.cf[:,-1]))/cmx
    if self.chebierr>stol:
        print(f'WARNING: Nr appeas to be too low (max|c_{{nmax,l}}|={self.chebierr:.2e})')
    if self.cheboerr>stol:
        print(f'WARNING: No appeas to be too low (max|c_{{nmax,l}}|={self.cheboerr:.2e})')
    if self.legerr>stol:
        print(f'WARNING: Nm appears to be too low (max|c_{{nLmax}}|={self.legerr:.2e})')
    return 

def updateResidual(self):
    '''
        updates the residual of the PDE
    '''    
    # find indices for interior pts where Theta-Phi_rot>0
    self.zi = np.where((self.thi-self.Phr)[self.ii]>0)[0]+self.ii[0] 

    # initialize residual vector:
    self.res = np.zeros([self.Nf*self.Nm+1])

    # apply Laplacian to current coefficients:
    lap = self.Lp.dot(self.cf.flatten())

    # interior grid pts: residual from generalized L-E eqn:
    self.res[self.ii+1] =-lap[self.ii] 
    self.res[self.zi+1]-= self.lm*self.lm*(self.thi-self.Phr)[self.zi]**self.n

    # exterior points: residual from Laplace's eqn: 
    self.res[self.oi+1] =-lap[self.oi]      

    # enforce normalization Theta=1 at r=mu=0:
    self.res[0] = 1. - self.thi[0] 
    
    # enforce homogeneous Neumann BC at r=0:
    self.res[1:self.Nm+1] = 0  

    # enforce continuity of Theta and its normal derivative at surface:
    self.res[1 + self.Nm*(self.Nr - 1):1 + self.Nm*self.Nr] = 0 
    self.res[1 + self.Nm*self.Nr:1 + self.Nm*(self.Nr + 1)] = 0 

    # Row with ro=inf, mu=0 fixes equatorial radius to r=1:
    self.res[1 + (self.Nf - 1)*self.Nm] = self.Phr[(self.Nr-1)*self.Nm] \
                                        - self.th[self.Nr-1,0] 
    return 

def updateJacobian(self):
    '''
        Constructs the Jacobian matrix required to compute the next 
        iterative refinement
    '''
    # for convenience:
    Nin = self.Nr*self.Nm
    
    # initialize new Jacobian matrix:
    self.JJ = np.zeros([self.Nf*self.Nm+1,self.Nf*self.Nm+1])

    # first row is an extra associated with new BC derived from eigenvalue
    # (homog. Dirichlet BC on correction at r=0):
    self.JJ[0,1:Nin+1] = np.kron(self.dri[0][0,:],self.dm[0][0]) 

    # first column is for the eigenvalue correction
    self.JJ[self.zi+1,0] = 2*self.lm*(self.thi-self.Phr)[self.zi]**self.n 

    # impose d delta/dr =0 at r=0:
    self.JJ[1:self.Nm+1,1:Nin+1] = np.kron(self.dri[1][0,:self.Nr],self.dm[0])

    # Laplacian imposed at all pts:
    self.JJ[self.Nm+1:,1:] = self.Lp[self.Nm:]

    # rest of LHS of variational equation imposed on interior points:
    self.JJ[self.zi+1,1:Nin+1]+= self.lm*self.lm*self.n*self.d0i[self.zi] \
                              *((self.thi-self.Phr)[self.zi,None])**(self.n-1.)
                               
    # impose continuity of delta at r=R_eq:
    self.JJ[1+Nin-self.Nm:1+Nin,:] = 0
    self.JJ[1+Nin-self.Nm:1+Nin,1:]= np.kron(self.dr[0][self.Nr-1] \
                                            -self.dr[0][self.Nr],self.dm[0])

    # impose continuity of d delta/dr at r=R_eq:
    self.JJ[1+Nin:1+Nin+self.Nm,:] = 0
    self.JJ[1+Nin:1+Nin+self.Nm,1:]=-np.kron(self.dr[1][self.Nr-1] \
                                            -self.dr[1][self.Nr],self.dm[0])

    # mu corresponding to r=inf,mu=0 used to fix equatorial radius to r=1:
    self.JJ[self.Nf*self.Nm+1-self.Nm,:] = 0
    self.JJ[self.Nf*self.Nm+1-self.Nm,1:Nin+1] = self.d0i[Nin-self.Nm]
    return 

############################################################################
############################# local methods ################################
############################################################################

def linsolve(A,b):
    '''
        numpy.linalg's solve used for simplicity/ease of installation. 
        Other linear algebra routines could easily be implemented here.
    '''
    return solve(A,b)