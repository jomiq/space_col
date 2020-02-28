import bpy
from bpy.props import   EnumProperty,           \
                        IntProperty,            \
                        FloatProperty,          \
                        FloatVectorProperty,    \
                        PointerProperty



import SCA
from SCA.util import Param as Param

from .PointGenerator import PointGenerator as PG

attractor_option_groups = {
    'NONE'      :    (),
    'SPHR'      :   (('N_pts', 'N'), ('R_pts', 'R'), ('C_pts','C')),
    'GAUSS'     :   (('N_pts', 'N'), ('sigma', 'σ'), ('mu', 'μ'), ('C_pts', 'C')),
    'SPHR_SURF' :   (('N_pts', 'N'), ('R_pts', 'R'), ('C_pts','C')),
    'CUBE'      :   (('N_pts', 'N'), ('R_pts', 'R'), ('C_pts','C')), 
    'TRI'       :   (('N_pts', 'N'),)
}

class SC_OT_add_space_col(bpy.types.Operator):
    bl_idname = "curve.add_space_col"
    bl_label = "Space Colonization"
    bl_description = "Grow me a tree"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    attractor_type: EnumProperty(
        name='attractor_type',
        description='Attractor point cloud shape',
        items=[
            ('NONE', 'Add attractor', '', 'ADD', 1),
            ('SPHR', 'Uniform spherical', '', 'SHADING_SOLID', 2),
            ('GAUSS', 'Gaussian spherical', '', 'SMOOTHCURVE', 3),
            ('SPHR_SURF', 'Uniform spherical surface', '', 'MESH_UVSPHERE', 4),
            ('CUBE', 'Unit cube', '', 'MESH_CUBE', 5),
            ('TRI', 'Uniform on triangle', '', 'OUTLINER_DATA_MESH', 6)
            ],
        default = 'NONE'   
    )

    selected_objects_attractor: EnumProperty(
        name='selected_objects_attractor',
        description='Object behaviour',
        items=[
            ('VERT', 'Vertices', '', 'MESH_DATA', 1),
            ('TRI', 'Uniform on triangles', '', 'OUTLINER_DATA_MESH', 2),
            ('GAUSS', 'Gaussian around surface', '', 'SMOOTHCURVE', 3)
            ],
        default = 'VERT'   
    )

    N_pts: IntProperty(
        name='N_pts',
        description='Number of attractor points',
        default=10,
        min=10,
        max=2000
    )

    R_pts: FloatProperty(
        name='R_pts',
        description='Radius of attractor',
        default=1.0,
        min=0.0,
        max=10.0
    )

    C_pts: FloatVectorProperty(
        name='C_pts',
        description='Center of attractor'
    )

    sigma: FloatProperty(
        name='sigma',
        description='Mean of radial distribution.',
        default=1.0,
        min=0.0
    )

    mu: FloatProperty(
        name='mu',
        description='Standard deviation',
        default=0.1,
        min=0.0
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text='Attractor')
        if bpy.context.selected_objects != []:
            box = layout.box()
            box.prop(self, 'selected_objects_attractor', text='Selected objects')

        box = layout.box()
        box.prop(self, 'attractor_type', text='Type')
        self.attractor_options(box)
        

        
    def attractor_options(self, box):
        for opt in attractor_option_groups[self.attractor_type]:
            box.prop(self, opt[0], text=opt[1])

        
