import bpy
from bpy.props import EnumProperty

import SCA
from SCA.util import Param as Param

from .PointGenerator import PointGenerator as PG

class SC_OT_add_space_col(bpy.types.Operator):
    bl_idname = "curve.add_space_col"
    bl_label = "Space Colonization"
    bl_description = "Grow me a tree"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    attractor_type: EnumProperty(
        name='attractor_type',
        description='Attractor point cloud shape',
        items=[
            ('SPHR', 'Uniform spherical', '', 'SHADING_SOLID', 1),
            ('GAUSS', 'Gaussian spherical', '', 'SMOOTHCURVE', 2),
            ('SPHR_SURF', 'Uniform spherical surface', '', 'MESH_UVSPHERE', 3),
            ('CUBE', 'Unit cube', '', 'MESH_CUBE', 4),
            ('TRI', 'Uniform on triangle', '', 'OUTLINER_DATA_MESH', 5),
            ('PARTICLE', 'Use emitter object', '', 'PARTICLES', 5)
            ],
        default = 'SPHR'
        
    )

    def execute(self, parameter_list):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.label(text='Attractor')
        box = layout.box()
        box.prop(self, 'attractor_type', text='Type')
        
