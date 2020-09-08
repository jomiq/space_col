# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "space_col",
    "author" : "Jomik",
    "description" : "Implementation of the space colonization algorithm for tree generation.",
    "blender" : (2, 81, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Add Curve"
}


import os
import sys 
dir = os.path.dirname('.')
if not dir in sys.path:
    sys.path.append(dir)

import bpy

from .space_col_op import SC_OT_add_space_col


def add_object_button(self, context):
    self.layout.operator(
        SC_OT_add_space_col.bl_idname,
        text="SPACE!",
        icon='PLUGIN')
        
def register():
    bpy.utils.register_class(SC_OT_add_space_col)
    bpy.types.VIEW3D_MT_curve_add.append(add_object_button)
    
def unregister():
    bpy.utils.unregister_class(SC_OT_add_space_col)
    bpy.types.VIEW3D_MT_curve_add.remove(add_object_button)
