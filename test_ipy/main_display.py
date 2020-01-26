
# %%
from IPython import get_ipython

# %%
import setpath
setpath.here()
# %%
%load_ext autoreload
%autoreload 2

import SCA
from PointGenerator import PointGenerator as PG
from SCA.util import Param as Param
from juputil.Plotters import tree_plot as T_plot, stat_plot as S_plot, dist_plot as D_plot

import numpy as np
from numpy.random import rand as rand

def vec(x,y,z):
    return np.array([x,y,z])
def rvec():
    return (rand(3)-0.5)*2

def prvec(axis=2, d=0):
    x = rvec()
    x[axis] = np.abs(x[axis]) + d
    return x


# %%


p_tri = [PG.triangular_uniform(prvec(d=0.2), prvec(d=0.2), prvec(d=0.2), N=10) for _ in range(100)]
pts = np.concatenate((*p_tri,))

r0 = rand(4,3)
r0[:,0] = 2*(r0[:,0] - 0.5)
r0[:,1] = 2*(r0[:,1] - 0.5)
r0[:,2] = 0


par = Param(r=0.03, kD=0.07, iD=0.2, bias=vec(0,0,0.2))
T = SCA.SpaceColony(points=pts, roots=r0, parameters=par, min_activation=5, trunk_lim=10, yeet_condition=20)


# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(80)\nT.walk()')


# %%
T_plot(T, decimate=True)

# %% 
T_plot(T, pointsize=20)


# %%
S_plot(T, True)


# %%
v = vec(0.0,0.0,2.5)
pts1 = PG.sphere(100, 1.5, v)
pts_tmp = PG.sphere_rad_gauss(100, 1.7, 0.01, v)
pts2 = [p for p in pts_tmp if p[2] > 1.2]
v = vec(0.7, 0.7, 1.0)
pts3 = PG.sphere(15, 0.5, v)
pts_tmp = PG.sphere_rad_gauss(30, 0.5, 0.01, v)
pts4 = [p for p in pts_tmp if p[2] > 1.0]

pts = np.concatenate((pts1, pts2, pts3, pts4))
# D_plot(pts, psize=2)


# %%
from SCA.util import normalize
par = Param(0.05, 0.7, 0.2, normalize(vec(0.0,0.0,1)))
T = SCA.SpaceColony(pts, parameters=par, trunk_lim=45, min_activation=41)
T.iterate(1000)
T.walk()

# %%
T_plot(T)

# %% 

T_plot(T, decimate=True)

# %%
S_plot(T, True)


# %%
# Stress test
pts = [p for p in PG.sphere_rad_gauss(N=10000, mu=1.0, sigma=0.05, C=vec(0,0,1)) if p[1] < 0.8]

par = Param(0.05, 0.4, 0.12, bias=vec(0,-0.7,0))
T = SCA.SpaceColony(points=pts, parameters=par, roots=np.array([[0,0,-0.3], [0,0,1.7]]), trunk_lim=30, maxsize=1000000, min_activation=20, yeet_condition=24)

# %%
D_plot(pts)

# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(800)\nT.walk()')


# %%

T_plot(T, pointsize=20)

# %%
T_plot(T, decimate=True)



# %%
S_plot(T, True)