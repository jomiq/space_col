import numpy as np
from numpy import pi
from numpy.random import *
from numpy.linalg import norm

def vector(x,y,z):
    return np.array([x,y,z])

def normalize(v):
    d = norm(v)
    if d == 0.0:
        return np.zeros_like(v)
    else:
        return np.divide(v, d)



class PointGenerator:
    two_pi = 2*pi

    '''Uniform distribution'''
    @classmethod
    def cube(cls, N=100, D=1.0, C=vector(0,0,0)):
        return D*(rand(N,3)-0.5) + C
    
    '''Uniform distributin in sphere'''
    @classmethod
    def sphere(cls, N=100, R=1.0, C=vector(0,0,0)):
        phi = rand(N)*cls.two_pi
        costheta = 2*rand(N) - 1
        theta = np.arccos(costheta)
        r = R*np.cbrt(rand(N))
        res = np.ndarray((N, 3))
        for i in range(N):
            res[i,0] = r[i] * np.sin(theta[i]) * np.cos(phi[i]) + C[0]
            res[i,1] = r[i] * np.sin(theta[i]) * np.sin(phi[i]) + C[1]
            res[i,2] = r[i] * costheta[i] + C[2]
        return res
    
    '''Uniform distributions on spherical surface'''
    @classmethod
    def sphere_surface(cls, N=100, R=1.0, C=vector(0,0,0)):
        res = cls.sphere(N, 1)
        for i in range(N):
            res[i] = R*normalize(res[i]) + C
        return res

    '''Uniform distribution in (theta, phi).''' 
    '''THe radial point density is gaussian.'''
    @classmethod
    def sphere_rad_gauss(cls, N=100, mu=0, sigma=0.1, C=vector(0,0,0)):
        phi = rand(N)*cls.two_pi
        costheta = 2*rand(N) - 1
        theta = np.arccos(costheta)
        r = normal(loc=mu, scale=sigma, size=N)
        res = np.ndarray((N, 3))
        for i in range(N):
            res[i,0] = r[i] * np.sin(theta[i]) * np.cos(phi[i]) + C[0]
            res[i,1] = r[i] * np.sin(theta[i]) * np.sin(phi[i]) + C[1]
            res[i,2] = r[i] * costheta[i] + C[2]
        return res

    def triangular_uniform(p1, p2, p3, N=1000):
        R = rand(N,2)
        # Let 
        u, v = p2 - p1, p3 - p1
        # then
        return np.array([p1 + np.sqrt(r[0])*(1-r[1])*u + (r[1]*np.sqrt(r[0])) * v for r in R])