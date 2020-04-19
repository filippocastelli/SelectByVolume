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
    "name" : "SelectByVolume",
    "author" : "Filippo Maria Castelli",
    "description" : "Select meshes by their volume",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.props import BoolProperty, FloatProperty, CollectionProperty

from .op import SelectByVolume_OT_Operator
from .panel import SelectByVolume_PT_Panel

classes = (SelectByVolume_OT_Operator,
           SelectByVolume_PT_Panel)

register, unregister = bpy.utils.register_classes_factory(classes)

bpy.types.Scene.sbv_use_multithread = BoolProperty(name="use multithreading",
                                                   description="Use multithreading for object selection, useful for large files.",
                                                   default=True)

bpy.types.Scene.sbv_use_cached = BoolProperty(name="use cached volumes",
                                                   description="Use cached volumes instead of calculating ex novo.",
                                                   default=True)

bpy.types.Scene.sbv_vol_max = FloatProperty(name="max volume",
                                            description="Max volume selected.",
                                            default=10000.)

bpy.types.Scene.sbv_vol_min = FloatProperty(name="min volume",
                                            description="Min volume selected.",
                                            default=0.)