import bpy

class SC_OT_add_space_col(bpy.types.Operator):
    bl_idname = "curve.add_space_col"
    bl_label = "Space Colonization"
    bl_description = "Grow me a tree"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, parameter_list):
        return {'FINISHED'}

    def draw(self, parameter_list):
        layout = self.layout
        print(layout)
        pass