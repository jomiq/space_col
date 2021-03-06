# %%
from IPython import get_ipython

import setpath
setpath.here()
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
