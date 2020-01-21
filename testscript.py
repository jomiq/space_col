import SCA
from numpy import array
from SCA.util import *
PG = SCA.PointGenerator

pts = PG.cube(500)
T = SCA.SpaceColony(pts, parameters=Param(0.05, 0.5, 0.1, array([0,0,0])))
T.iterate(500)
T.walk()

print(T)

T.stop()
print(T)
T.__del__()