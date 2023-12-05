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
# Module: pseudo
# Brief: subroutines for initializing pseudospectral grids/matrices
############################################################################

import numpy as np
from scipy.special import lpmv
from numpy.linalg import inv
from numpy.polynomial.legendre import leggauss 

############################################################################
################### Methods to be imported into client #####################
############################################################################

def setGrid(self):
    '''
        constructs 1D pseudospectral grids and 2D meshes for the model
    '''

    # interior radial grids and dmats:
    self.xi,self.ri,self.rpi,self.rw = glbGrid(self.Nr,0,1.)

    # exterior radial grid:
    self.xo = glbGrid(self.No)[0]
    self.ro = np.append(2./(1 + self.xo[:-1]),np.inf) # map [1,-1] -> [1,inf]
    self.rr = np.append(self.ri,self.ro) # full radial grid on [0,inf]
    self.Nf = self.rr.size

    self.mu,self.mw = legaussGrid(self.Nm,parity=1)
    self.ss = np.sqrt(1. - self.mu**2)
    self.Nm = self.mu.size
    self.ll = np.arange(0,2*self.Nm,2)

    # Cylindrical radius and polar axis meshes:      
    self.R = self.rr[:,None]*self.ss[None,:]
    self.z = np.zeros_like(self.R)
    self.z[:-1] = self.rr[:-1,None]*self.mu[None,:]
    self.z[-1,:]= np.inf

    # indices for grid points r\in(0,1)
    self.ii = np.arange(self.Nm,self.Nm*(self.Nr-1)) 

    # indices for pts r\in(1,inf)
    self.oi = np.arange(self.Nm,self.Nm*self.No) + self.Nr*self.Nm 

    # 2D spectral weights;
    self.ww = (self.ri**2*self.rw)[:,None]*self.mw[None,:]*4*np.pi
    return 

def setMats(self):
    '''
        constructs 1D pseudospectral differentiation matrices:
    '''
    # interior radial derivatives:
    self.dri = makeDmats([Tn,dTn,d2Tn],self.xi,self.rpi)

    # exterior radial derivatives (scaled for map [1,-1] --> [1,inf]):
    dro = makeDmats([Tn,dTn,d2Tn],self.xo,1.)
    self.dro = [dro[0]]
    self.dro.append((-0.5*(1. + self.xo)**2)[:,None]*dro[1]) 
    self.dro.append((0.25*(1. + self.xo)**4)[:,None]*dro[2] \
                   +( 0.5*(1. + self.xo)**3)[:,None]*dro[1])

    # combined interior/exterior radial derivative mats:
    self.dr = []
    for i in range(3):
        self.dr.append(np.zeros([self.Nf,self.Nf]))
        self.dr[i][:self.Nr,:self.Nr] = self.dri[i]
        self.dr[i][self.Nr:,self.Nr:] = self.dro[i]

    # inversion matrix:
    self.dii = inv(self.dr[0])

    self.dm = makeDmats([Pl,dPl],self.mu,1.,par=1)
    self.dmi= inv(self.dm[0])
    return 

def set2Dops(self):
    '''
        constructs a few 2D operators (wasteful use of memory, but 
        they're useful during the Newton iteration)
    '''
    # zero'th order derivative:
    self.d0i= np.kron(self.dri[0],self.dm[0]) 

    # Laplacian operator:
    ll1 = self.ll*(self.ll+1)
    ir = 1./self.rr[1:]
    self.Lp = np.zeros([self.Nf*self.Nm,self.Nf*self.Nm])
    self.Lp[self.Nm:] = np.kron(self.dr[2][1:] \
              + (2.*ir)[:,None]*self.dr[1][1:],self.dm[0]) \
      - np.kron((ir*ir)[:,None]*self.dr[0][1:],ll1[None,:]*self.dm[0])
    return 

def gridToCoeff(self):
    '''
        maps grid-point evaluations of Theta(r,theta) to spectral 
        coefficients
    '''
    self.cf = self.dii.dot(self.dmi.dot(self.th.T).T)
    self.cfi= self.cf[:self.Nr,:].flatten()
    return 

def coeffToGrid(self):
    '''
        maps spectral coefficients to grid-point evaluations of 
        Theta(r,theta)
    '''
    self.th = self.dr[0].dot(self.dm[0].dot(self.cf.T).T)
    self.thi= self.th[:self.Nr,:].flatten()
    return 

############################################################################
################### Pseudospectral grid constructors #######################
############################################################################

def glbGrid(N,ymin=-1.,ymax=1.):
    '''
        calculates Gauss-Lobatto grid comprising endpoints and extrema of 
        Chebyshev polynomialself. Applies a linear transformation to remap from 
        [1,-1] --> [ymin,ymax]

        Inputs: 
            - N:  number of grid points
            - ymin,ymax: end-points of desired domain
        Outputs:
            - xx: grid-point values on [1,-1] (used to evaluate Chebyshevs)
            - yy: remapped points y=y(x) on [ymin,ymax]
            - yp: derivative y'=dy/dx associated with linear mapping y=y(x)
            - ww: weights for Clenshaw-Curtis quadrature
    '''
    # grid-points on [1,-1] 
    tt = np.pi*np.arange(N)/(N-1)
    xx = np.cos(tt)

    # Clenshaw-Curtis quadrature weights [see Boyd (2001), pp. 456)]
    mm = np.arange(1,N-1)
    arr= 2*np.sin(tt[None,:])*np.sin(mm[:,None]*tt[None,:]) \
          *(1. - np.cos(mm[:,None]*np.pi))/mm[:,None]/(N-1)
    ww = np.sum(arr,axis=0)
    ww*=(ymax - ymin)/2.
    
    # rescale to new bounds:
    yy = (1. - xx)*(ymax - ymin)/2. + ymin
    yp =-(ymax - ymin)/2.
    return xx,yy,yp,ww

def legaussGrid(N,parity=1):
    '''
        computes grid/weights for Gaussian quadrature involving
        Legendre polynomialself.
    '''
    # compute grid/weights for full meridional plane:
    mu,mw = leggauss(2*N+1)

    # halve and adjust weights to only include mu\in[0,1]
    mw = 0.5*(mw[N:] + mw[N::-1])
    mw[0]/= 2
    mu = mu[N:]
    return mu,mw

############################################################################
################## Basis function evaluation functions #####################
############################################################################

def Tn(x,n):
    '''
        Computes Chebyshev polynomials of (possibly vectorized) order n,
        evaluated at (possibly vectorized) x in [1,-1], using Trigonometric 
        form Tn(x)=Tn(cos(t))=cos(n*t)
    '''

    if np.any(abs(x)>1.): 
        raise ValueError('x must be a value in [-1,1]')

    return np.cos(n*np.arccos(x))

def dTn(x,n):
    '''
        first derivative of Tn wrt. x (analytical formula used for |x|==1).
    '''
    if np.any(abs(x)>1.): 
        raise ValueError('x must be a value in [-1,1]')

    t = np.arccos(x)
    ss= np.sin(t)
    if type(x)==np.ndarray:
        Tnx = np.zeros_like(x)
        intr,bdry = (abs(x)<1.),(abs(x)==1.)
        Tnx[intr] = (n*np.sin(n*t))[intr]/ss[intr]
        Tnx[bdry] = (np.sign(x)**(n+1)*n*n)[bdry]
    else:
        Tnx = n*np.sin(n*t)/ss if abs(x)<1. else np.sign(x)**(n+1)*n*n

    return Tnx

def d2Tn(x,n):
    '''
        second derivative of Tn wrt. x
    '''

    if np.any(abs(x)>1.): 
        raise ValueError('x must be a value in [-1,1]')

    t = np.arccos(x)
    ss= np.sin(t)
    cc= np.cos(t)

    if type(x)==np.ndarray:
        Tnxx = np.zeros_like(x)
        intr,bdry = (abs(x)<1.),(abs(x)==1.)
        Tnxx[intr] =(-n*n*np.cos(n*t))[intr]/ss[intr]/ss[intr] \
                   +(n*np.sin(n*t)*cc)[intr]/ss[intr]/ss[intr]/ss[intr]
        Tnxx[bdry] =(np.sign(x)**(n+2)*n*n*(n*n - 1.)/3.)[bdry]
    else:
        if abs(x)==1:
            Tnxx = np.sign(x)**(n+2)*n*n*(n*n - 1.)/3
        else:
            Tnxx = -n*n*np.cos(n*t)/ss/ss + n*np.sin(n*t)*cc/ss/ss/ss
    return Tnxx

def Pl(mu,l):
    '''
        Computes zonal Legendre polynomial of degree l, evaluated at mu
    '''

    if np.any(abs(mu)>1.): 
        raise ValueError('mu must be a value in [-1,1]')

    return lpmv(0,l,mu)

def dPl(mu,l):
    '''
        Uses recursion relation to compute first derivative of Legendres
    ''' 

    if np.any(abs(mu)>1.): 
        raise ValueError('mu must be a value in [-1,1]')

    return (l*lpmv(0,l-1,mu) - l*mu*lpmv(0,l,mu))/(1 - mu**2)


############################################################################
##################### Collocation matrix constructor #######################
############################################################################

def makeDmats(dfuns,x,yp,par=0,n0=0,**kwargs):
    '''
        computes pseudospectral collocation matriceself. 

        Inputs:
            -dfuns: list of functions for computing basis function derivs
                    (d^0/dx^0,d^1/dx^1,...). Each function must be of form
                    f(x,n), where x and n are the grid points and basis 
                    function orders for evaluation (resp.). functions must 
                    be capable of accepting x and n in mesh form
            -x:     array of grid points for evaluation. 
            -yp:    derivative y' for transformation y=y(x).
            -par:   assumed parity with respect to first endpoint in x 
                    -1 for odd-parity, 1 for even, assumes no parity for 
                    any other option
            -n0     initial starting order
        Outputs:
            -dmats: list [dm_inv,d0,d1,d2...] where dm_inv computes coeff-
                    cients from grid-points, and d0,d1,d2,... compute grid
                    point evaluations from nth order derivatives
    '''
    # make meshes of grid-points and basis orders:
    N = x.size
    if par==1:
        n = np.arange(n0,n0+2*N,2) 
    elif par==-1:
        n = np.arange(n0+1,n0+1+2*N,2)
    else:
        n = np.arange(n0,n0+N)
    X,N = np.meshgrid(x,n,indexing='ij')

    # check to make sure yp is not an array:
    if hasattr(yp,"__len__"):
        raise ValueError('dy/dx for mapping y=y(x) cannot be array-like')

    # make/return list of pseudospectral matrices:
    return [dfun(X,N,**kwargs)*(1./yp)**j for j,dfun in enumerate(dfuns)]