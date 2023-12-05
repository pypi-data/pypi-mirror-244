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
# Module: rotpot
# Brief: subroutines for integration of effective centrifugal potential
############################################################################

import numpy as np
from .pseudo import glbGrid
from .helpers import terp

############################################################################
################### Methods to be imported into client #####################
############################################################################

def setPhiRot(self):
    ''' 
        Given either a constant angular velocity Omega, or a function
        depending on cylindrical R, computes the centrifugal potential 

                    Phi_rot = - int_0^R x*Omega^2(x)dx
    '''
    if isinstance(self.Om,float) or isinstance(self.Om,int):
        # no differential rotation --> very simple Phi_rot:
        self.Om  = self.Om*np.ones_like(self.R[:self.Nr])
        self.dOd1= np.zeros_like(self.ri)
        self.dOdR= np.zeros_like(self.Om)
        self.Phr =-0.5*self.R[:self.Nr]**2*self.Om**2
        self.dPhdR =-self.R[:self.Nr]*self.Om**2
    elif callable(self.Om):
        # compute Phi_rot:
        if callable(self.Phr):
            self.Ph1d= Phr(self.ri)
            self.Phr = Phr(self.R[:self.Nr])
        else:
            if self.vrb: 
                print('integrating Phi_rot numerically')
            x,r,rp,w = glbGrid(self.Ni,-1,1)
            X,R = np.meshgrid(x,self.ri[1:],indexing='ij')
            W = np.meshgrid(w,self.ri[1:],indexing='ij')[0]*R/2.
            Y = (1. - X)*R/2.
            self.Ph1d= np.append(0,-np.sum(Y*self.Om(Y)**2*W,axis=0))
            self.Phr = np.array([
                        terp(self.ri,self.Ph1d,self.R[:self.Nr,j]) \
                        for j in range(self.Nm)]).T

            # set Om to 2D grid evaluation (on interior grid):
            self.Om = self.Om(self.R[:self.Nr])
    else:
        raise ValueError('Om must be float or function Om(R=r*sin th)')
        
    # more useful form for iteration:
    self.Phr = self.Phr.flatten()
    return 


