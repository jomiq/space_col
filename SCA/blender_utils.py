from .util import *
from .SpaceColony import SpaceColony
import bpy

def to_mesh(T:SpaceColony, start=-1, end=-1):
    if start == -1:
        start = 0
    
    if end == -1:
        end = T.end

    verts = [(T.nodes[i,0]), T.nodes[i,1], T.nodes[i,2]) for i in range(start, end)]
    edges = T.edges
    
    mesh = bpy.data.meshes.new("tree")
    mesh.from_pydata(verts, T.edges, [])

def get_