import numpy as np 
from numpy.linalg import norm
from collections import namedtuple

def as_numpy_arr(shape, shared_obj, dtype=np.float):
    return np.ndarray(shape, dtype=dtype, buffer=shared_obj.buf)

def normalize(v):
    d = norm(v)
    if d == 0.0:
        return np.zeros_like(v)
    else:
        return np.divide(v, d)

Batch = namedtuple('Batch', 'run, func, args')
Param = namedtuple('Param', 'r, iD, kD, bias')
Stats = namedtuple('Stats', 'sz, act, reached_points')