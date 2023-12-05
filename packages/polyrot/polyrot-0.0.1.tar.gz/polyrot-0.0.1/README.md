# Polyrot

This package computes the equilibrium structure of rotating planets and stars modelled as "polytropes" with pressure and density related by $P\propto \rho^{1 + 1/n}$ (where $n$ is a "polytropic index"). Specifically, polyrot solves the partial differential equation

$$
    \nabla^2\Theta
    =-\lambda^2 \left(\Theta-{\Phi}_\text{rot}\right)^n,
$$

where (in spherical coordinates $r,\theta,\phi$) $\Theta(r,\theta)$ is an axisymmetric (but not spherically symmetric) Lane-Emden variable related to the gravitational potential of the star, $\lambda$ is an eigenvalue associated with the spatial scale of the body (see Boyd, 2011), and 

$$
  \Phi_\text{rot}
  =-\int_0^Rx\Omega^2(x)\text{d}x
$$

is an effective centrifugal potential determined by the angular velocity profile $\Omega=\Omega(R)$ (where $R=r\sin\theta$ is the cylindrical radius). For more details, please see Dewberry, Mankovich & Fuller (2022; https://ui.adsabs.harvard.edu/abs/2022MNRAS.516..358D/abstract).

## Installation
This package should require only an installation of numpy, scipy, and matplotlib. The code can be pip-installed with 

```
  pip install polyrot
```

## Usage
The jupyter-notebook included in this repository introduces basic usage of polyrot. 

## License
Copyright (C) 2023 Janosz Dewberry

polyrot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

polyrot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Citation
If you make use of Polyrot for any publications, please link to the code repository at <https://github.com/dewberryjanosz/polyrot>, and include a citation to

Dewberry, J. W., Mankovich, C. R., & Fuller, J. 2022, MNRAS, 516, 358 (DOI: 10.1093/mnras/stac1957)
