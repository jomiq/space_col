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

# %%

# %%
'''Produces the closest unit vector'''
def grow_max(v):
    i = np.where(abs(v)==np.amax(np.abs(v)))[0]
    res = np.zeros(3)
    res[i] = 1.0*float(np.sign(v[i]))
    return res

pts = PG.sphere(N=700,R=1.0, C=vec(0,0,1.5))
par = Param(0.1, 0.5, 0.1, vec(0,0,0.5))
T = SCA.SpaceColony(points=pts, parameters=par, trunk_lim=10, grow_function=grow_max)


# %%
T.iterate(600)
# %%
S_plot(T)
# %%
T.walk()
T_plot(T)
# %%
