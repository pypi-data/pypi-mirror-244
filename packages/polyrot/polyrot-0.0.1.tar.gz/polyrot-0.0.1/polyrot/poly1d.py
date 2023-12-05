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
# Module: poly1d
# Brief: computes initial iteration from 1D Lane-Emden equation
############################################################################

import numpy as np 
from numpy.linalg import solve

############################################################################
################### Methods to be imported into client #####################
############################################################################

def computeICs(self,itmax=100,tol=1e-15):
    '''
        computes an initial guess for computing 2D, rotating polytropes,
        taken as the 1D solution to the nonrotating Lane-Emden equation
        (computed essentially as described in Boyd 2011). Mainly useful for 
        the eigenvalue, since otherwise the Newton step in the 2D 
        computation starts out much larger than it needs to be. 
    '''
    if self.vrb:
        print('')
        print('###########################################################')
        print('### Solving 1D Lane-Emden equation for initial solution ###')
        print('###########################################################')
        print('')

    # for convenience:
    N,rr,nn = self.Nr,self.rr,self.n
    d0,d1,d2= self.dr

    # set initial guesses for eigenfun and val:
    yy = np.append(np.cos(np.pi*self.ri/2.),
                  (np.sin(np.pi/2.)/self.ro-1.)*np.pi/2.)
    aa = solve(d0,yy)
    dy = d1.dot(aa)
    lm = 3.

    # Newton iteration:
    itr = 0
    while itr<itmax:
        # compute residual vector:
        resid = np.zeros([self.Nf+1])
        resid[2:]=-d2.dot(aa)[1:] - 2*dy[1:]/rr[1:]
        resid[2:N+1]-= lm*lm*abs(yy[1:N])**nn

        # compute Jacobian matrix:
        J = np.zeros([self.Nf+1,self.Nf+1])

        # coefficients for the correction eps to the eigenvalue:
        J[2:N+1,0] = 2*lm*abs(yy[1:N])**nn 
        
        # coefficients for the correction dl to the solution:
        J[2:,1:] = d2[1:] + (2./rr[1:])[:,None]*d1[1:]
        J[2:N+1,1:N+1]+= lm*lm*nn*((abs(yy[:N])**(nn-1))[:,None] \
                                 *self.dri[0])[1:]

        # impose boundary/interface conditions on correction. First
        # homog. Dirichlet IBC:
        J[0,1:N+1] = self.dri[0][0,:]
        resid[0] = 1. - yy[0]  
        
        # homog. Neumann IBC (irrelevant w/par==1):
        J[1,1:N+1] = self.dri[1][0,:] 
        resid[1] = 0      

        # homog. Dirichlet BC at r=R_eq:
        J[-1,1:N+1]= self.dri[0][-1,:]
        resid[-1]= 0           

        # interface BC on derivative:
        J[N,1:N+1]= self.dri[0][-1,:]
        J[N,N+1:] =-self.dro[0][0,:]
        resid[N]  = 0  

        # interface BC on solution:
        J[N+1,1:N+1]=-self.dri[1][-1,:]
        J[N+1,N+1:] = self.dro[1][0,:]
        resid[N+1]  = 0 
              
        # solve for correction (to both soln and evalue)
        dl = solve(J,resid)
        lm+= dl[0]
        aa+= dl[1:]

        # transform coeffs to grid-pt vals
        yy,dy = d0.dot(aa),d1.dot(aa)
        
        # print status, if running in loud mode:
        if self.vrb: 
            status = f'iter {itr}: lam={lm:.4f}, dlam/lam={dl[0]/lm:.2e}, '
            status+= f'max[resid]={np.amax(abs(resid)):.2e}'
            print(status)

        # check for convergence:
        if np.amax(abs(dl))<tol or np.amax(abs(resid))<tol: 
            break
        itr+=1

    # raise error if convergence failed:
    if itr>=itmax:
        raise ValueError(f'1D sol. failed to converge after {itr} iters')

    # set initial 1D solution from 2D:
    self.lm = lm # eigenvalue (main point of this calculation)
    self.th = np.meshgrid(yy,self.mu,indexing='ij')[0]
    self.thi= self.th[:self.Nr,:].flatten()
    self.gridToCoeff()
    return 