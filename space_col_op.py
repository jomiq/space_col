import bpy
from bpy.props import EnumProperty

import SCA
from SCA.util import Param as Param
from SCA.PointGenerator import PointGenerator as PG

class SC_OT_add_space_col(bpy.types.Operator):
    bl_idname = "curve.add_space_col"
    bl_label = "Space Colonization"
    bl_description = "Grow me a tree"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    attractor_type: EnumProperty{
        name='attractor_type',
        description='Attractor point cloud shape',
        items=[
            ('SPHR', 'Uniform spherical', '', 'SHADING_SOLID'),
            ('GAUSS', 'Gaussian spherical', '', 'SMOOTHCURVE'),
            ('SPHR_SURF'), 'Uniform spherical surface', 'MESH_UVSPHERE'
            ('CUBE', 'Unit cube', '', 'MESH_CUBE'),
            ('TRI', 'Uniform on triangle', '', 'OUTLINER_DATA_MESH')
            ('PARTICLE', 'Use emitter object', '', 'PARTICLES')
            ],
            default = 'SPHR'
        ]
    }

    def execute(self, parameter_list):
        return {'FINISHED'}

    def draw(self, parameter_list):
        layout = self.layout
        print(layout)
        pass