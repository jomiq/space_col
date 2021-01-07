# %%
from IPython import get_ipython

# %%
import setpath
setpath.here()


# %%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

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

# %% [markdown]
# # !!!

# %%
p_tri = [PG.triangular_uniform(prvec(d=0.2), prvec(d=0.2), prvec(d=0.2), N=10) for _ in range(100)]
pts = np.concatenate((*p_tri,))

r0 = rand(10,3)
r0[:,0] = 1.5*(r0[:,0] - 0.5)
r0[:,1] = 1.5*(r0[:,1] - 0.5)
r0[:,2] = 0


par = Param(r=0.03, kD=0.07, iD=0.2, bias=vec(0,0,0.9))
T = SCA.SpaceColony(points=pts, roots=r0, parameters=par, min_activation=5, trunk_lim=10, yeet_condition=20)

# %%
T.iterate(80)

# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(80)\nT.walk()')


# %%
T.walk()
T_plot(T, pointsize=20)


# %%
T_plot(T, decimate=True)


# %%
S_plot(T, True)

# %% [markdown]
# # !!!

# %%
v = vec(0.0,0.0,2.5)
pts1 = PG.sphere(100, 1.5, v)
pts_tmp = PG.sphere_rad_gauss(200, 1.7, 0.01, v)
pts2 = [p for p in pts_tmp if p[2] > 1.2]
v = vec(0.7, 0.7, 1.0)
pts3 = PG.sphere(15, 0.5, v)
pts_tmp = PG.sphere_rad_gauss(60, 0.5, 0.01, v)
pts4 = [p for p in pts_tmp if p[2] > 1.0]

pts = np.concatenate((pts1, pts2, pts3, pts4))

par = Param(0.05, 0.7, 0.2, vec(0.0,0.0,-0.9))
T = SCA.SpaceColony(pts, parameters=par, trunk_lim=55, min_activation=50, yeet_condition=5)


# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(1000)\nT.walk()')


# %%
T_plot(T, pointsize=20)


# %%
T_plot(T, decimate=True)


# %%
S_plot(T, True)

# %% [markdown]
# # !!!

# %%
pts = [p for p in PG.sphere_rad_gauss(N=10000, mu=1.0, sigma=0.05, C=vec(0,0,1)) if p[1] < 0.8]

par = Param(0.05, 0.4, 0.12, bias=vec(0,-0.7,0))
T = SCA.SpaceColony(points=pts, parameters=par, roots=np.array([[0,0,-0.3], [0,0,1.7]]), trunk_lim=30, maxsize=1000000, min_activation=20, yeet_condition=24)


# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(800)\nT.walk()')


# %%
T_plot(T, pointsize=20)


# %%
T_plot(T, decimate=True)


# %%
S_plot(T, True)


# %%
pts = np.concatenate([PG.sphere_surface(N=15000), PG.sphere_surface(N=15000, R=0.5)])
rts = PG.sphere_surface(N=7, R=0.75)
par = Param(0.04, 0.2, 0.08, bias=vec(0,0,0))
T = SCA.SpaceColony(points=pts, parameters=par, roots=rts, trunk_lim=120, maxsize=1000000, min_activation=20, yeet_condition=24)


# %%
get_ipython().run_cell_magic('time', '', 'T.iterate(200)')


# %%
T.walk()
T_plot(T, pointsize=20, show_leaves=False)


# %%
T_plot(T, decimate=True)


# %%
S_plot(T, normal_to_size=True)

# %%
pts = PG.sphere(N=800,R=1.0, C=vec(0,0,1.5))
par = Param(0.03, 0.8, 0.1, vec(0,0,0.1))
T = SCA.SpaceColony(points=pts, parameters=par, trunk_lim=10)


# %%
T.iterate(6000)
# %%
S_plot(T)
# %%
T.walk()
T_plot(T)
# %%
