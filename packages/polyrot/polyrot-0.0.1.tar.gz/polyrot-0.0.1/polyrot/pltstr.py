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
# Module: pltstr
# Brief: plotting function definitions
############################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.axes_grid1 import make_axes_locatable

############################################################################
################### Methods to be imported into client #####################
############################################################################

def plotPolyStar(self,log=False,cmaps=['plasma','inferno','viridis'],
    cnorm=1e7):
    '''
        Generates a plot with panels showing (i) slices of Theta-Phi_rot 
        along rays of constant latitude, (ii) a heatmap of the spectral 
        coefficient amplitudes, and (iii) a cross-section showing the 
        density and surface radius. 
    '''

    # (temporarily) overide defaults:
    ofs = plt.rcParams['font.size']
    plt.rcParams.update({'font.size':14})
    with plt.style.context('dark_background'):

        # initialize plot:
        f,ax = plt.subplots(1,3,figsize=(12.8,4.4))

        # line plot showing slices of theta - Phi_rot along rays:        
        muval = np.array([self.mu[j*int(self.Nm/8)] for j in range(9)])
        dev = self.th[:self.Nr] - self.Phr.reshape([self.Nr,self.Nm])
        deval = np.array([dev[:,j*int(self.Nm/8)] for j in range(9)])
        dvcol = plt.get_cmap(cmaps[0])(np.linspace(0,0.95,len(muval)))
        for j,mu in enumerate(muval):
            ax[0].plot(self.ri,deval[j],color=dvcol[j])
        ax[0].plot([0,1],[0,0],'w-')
        # add colorbar indicating which slice is where:
        div = make_axes_locatable(ax[0])
        cax = div.append_axes('top', size='5%', pad=0)
        yt = muval
        ytl= [f'{m:.1f}' for m in muval]
        ytl[1::2] = ['' for _ in range(len(ytl[1::2]))]
        cbr = ColorbarBase(cax,cmap=plt.get_cmap(cmaps[0]),values=yt,
                           orientation='horizontal',ticks=yt)
        cbr.ax.set_xticklabels(ytl,fontsize=10)
        cbr.ax.set_xlabel('$\\mu=\\cos\\theta$',fontsize=14)
        cbr.ax.xaxis.set_ticks_position('top')
        cbr.ax.xaxis.set_label_position('top')
        ax[0].set_xlim([0,1])
        ax[0].set_ylim([-.1,np.amax(dev)*1.05])
        ax[0].set_xlabel('$r/R_{eq}$')
        ax[0].set_ylabel('$[\\Theta - \\Phi_{rot}](r,\\mu)$')
        
        # heatmap showing tensor basis coefficients:
        mxc= np.amax(abs(self.cf))
        im1= ax[1].imshow(abs(self.cf).T,aspect='auto',cmap=cmaps[1],
                          norm=LogNorm(vmin=mxc/cnorm,vmax=mxc))        
        div2 = make_axes_locatable(ax[1])
        cax2 = div2.append_axes('top', size='5%', pad=0)        
        plt.colorbar(im1,cax=cax2,label='$c_{nl}$',pad=0,location='top',
                     orientation='horizontal')
        ax[1].set_xlabel('Chebyshev order $n$')
        xt = [0,int(self.Nr/4),int(self.Nr/2),int(self.Nr*3/4),
              self.Nr,self.No+self.Nr-1]
        xtl= [f'{n}' for n in 
             [0,int(self.Nr/4),int(self.Nr/2),int(self.Nr*3/4),0,self.No-1]]
        ax[1].set_xticks(xt)
        ax[1].set_xticklabels(xtl)
        ax[1].set_ylabel('Legendre degree $\\ell$')
        lstep = max(int(self.Nm/20),1)
        yt = np.arange(0,self.Nm,2*lstep)
        ytl= [f'{l}' for l in np.arange(0,2*self.Nm,4*lstep)]
        ax[1].set_yticks(yt)
        ax[1].set_yticklabels(ytl)
        xlim,ylim = [-0.5,self.cf.shape[0]-0.5],[-0.5,self.cf.shape[1]-0.5]
        ax[1].set_xlim(xlim)
        ax[1].set_ylim(ylim)
        ax[1].plot([self.Nr-0.5,self.Nr-0.5],ylim,'w-')
        ax[1].text(lstep,ylim[-1]-lstep*2,'$r<R_{eq}$',fontsize=10)
        ax[1].text(self.Nr+0.5,ylim[-1]-lstep*2,'$r>R_{eq}$',fontsize=10)

        # colorplot showing cross-section of density:
        x,z = quadmesh(self.R[:-1],self.z[:-1])
        rho = np.concatenate((self.rho,np.zeros([self.No-1,self.Nm])),axis=0)
        rho = np.concatenate((rho[:,1:][:,::-1],rho),axis=1)
        if log:
            im2 = ax[2].pcolormesh(x,z,rho,cmap=cmaps[2],
                                   norm=LogNorm(vmin=1/1e10,vmax=1.))
            ax[2].pcolormesh(-x,z,rho,cmap=cmaps[2],
                             norm=LogNorm(vmin=1/1e10,vmax=1.))
        else:
            im2 = ax[2].pcolormesh(x,z,rho,cmap=cmaps[2])
            ax[2].pcolormesh(-x,z,rho,cmap=cmaps[2])
        div3 = make_axes_locatable(ax[2])
        cax3 = div3.append_axes('top', size='5%', pad=0)       
        plt.colorbar(im2,cax=cax3,label='$\\rho(r,\\theta)/\\rho_c$',pad=0,
                     location='top',orientation='horizontal')
        plt.sca(ax[2])
        plt.axis('equal')
        ax[2].set_xlim([-1.1,1.1])
        ax[2].set_ylim([-1.1,1.1])
        ax[2].set_xlabel('$x/R_{eq}$')
        ax[2].set_ylabel('$z/R_{eq}$')

        # plot surface radius:
        mu = np.append(self.mu,1.)
        ss = np.sqrt(1. - mu**2)
        rs = np.append(self.rs,[self.Rp])
        ax[2].plot(ss*rs, mu*rs,'w-',-ss*rs, mu*rs,'w-',
                   ss*rs,-mu*rs,'w-',-ss*rs,-mu*rs,'w-')

        # adjust spacing:
        plt.subplots_adjust(top=0.85,bottom=0.155,wspace=0.25,left=0.065,
            right=0.99)

    # show figure:
    plt.show()

    # reset plt default font size:
    plt.rcParams.update({'font.size':ofs})
    return 

############################################################################
############################# local methods ################################
############################################################################

def quadmesh(xc,zc):
    '''
        generates quadrilateral mesh for plotting with matplotlib's 
        pcolormesh (to eliminate slices at poles)
    '''
    Nr,Nm = xc.shape
    xc = np.concatenate((xc[:,1:][:,::-1],xc),axis=1)
    zc = np.concatenate((-zc[:,1:][:,::-1],zc),axis=1)

    # make quadrilateral meshes covering cell edges:
    x = np.zeros([Nr+1,Nm*2])
    z = np.zeros([Nr+1,Nm*2])
    x[1:-1,1:-1] = 0.25*(xc[:-1,:-1] + xc[1:,:-1] + xc[:-1,1:] + xc[1:,1:])
    z[1:-1,1:-1] = 0.25*(zc[:-1,:-1] + zc[1:,:-1] + zc[:-1,1:] + zc[1:,1:])
    x[:,0] = 0
    x[:,-1]= 0
    x[0,:] = 0
    x[-1,:]= x[-2,:]
    z[0,:] = 2*z[1,:] - z[2,:]
    z[-1,:]= 2*z[-2,:]- z[-3,:]
    z[:,0] = z[:,1]
    z[:,-1]= z[:,-2]
    return x,z
