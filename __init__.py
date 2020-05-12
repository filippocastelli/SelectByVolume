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
    "version" : (0, 2, 2),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
 
from bpy.props import BoolProperty, FloatProperty, CollectionProperty, IntProperty, StringProperty, CollectionProperty, PointerProperty
from .property_groups import MaterialGroup, InputFieldGroup, ColormapGroup
from .select_volume_op import SelectByVolume_OT_Operator
from .multi_selection_op import AddInputField_OT_Operator, ResetFields_OT_Operator, RemoveInputField_OT_Operator, ApplyMaterials_OT_Operator, SelectChunk_OT_Operator, GenerateSpaced_OT_Operator
from .material_op import ApplyAllMaterials_OT_Operator, ApplyColormap_OT_Operator, RandomizeColors_OT_Operator
from .panel import SelectByVolume_PT_Panel

# REGISTERING / UNREGISTERING  CLASSES

# custom PropertyGroups must be registered before being used
# by including them in register_classes_factory() the rest of the __init__.py
# would be executed before InputFieldGroup has a chance to be registered

# CUSTOM PROPS REGISTERING
bpy.utils.register_class(InputFieldGroup)
bpy.utils.register_class(MaterialGroup)
bpy.utils.register_class(ColormapGroup)

classes = (SelectByVolume_OT_Operator,
           SelectByVolume_PT_Panel,
           AddInputField_OT_Operator,
           RemoveInputField_OT_Operator,
           ResetFields_OT_Operator,
           SelectChunk_OT_Operator,
           ApplyMaterials_OT_Operator,
           ApplyColormap_OT_Operator,
           ApplyAllMaterials_OT_Operator,
           RandomizeColors_OT_Operator,
           GenerateSpaced_OT_Operator
           )

fac_register, fac_unregister = bpy.utils.register_classes_factory(classes)

def register():
    fac_register()

def unregister():
    fac_unregister()
    #bpy.utils.unregister_class(InputFieldGroup)
    #del(bpy.types.Scene.sbv_use_multithread)
    #del(bpy.types.Scene.sbv_use_cached)
    #del(bpy.types.Scene.sbv_vol_max)
    #del(bpy.types.Scene.sbv_vol_min)
    #del(bpy.types.Scene.inputfields)


# INITIALIZING PROPS / PROPGROUPS
bpy.types.Scene.sbv_use_multithread = BoolProperty(name="use multithreading",
                                                   description="Use multithreading for object selection, useful for large files.",
                                                   default=False)

bpy.types.Scene.sbv_use_cached = BoolProperty(name="use cached volumes",
                                                   description="Use cached volumes instead of calculating ex novo.",
                                                   default=True)

bpy.types.Scene.sbv_vol_max = FloatProperty(name="max volume",
                                            description="Max volume selected.",
                                            min=0.,
                                            default=500.)

bpy.types.Scene.sbv_vol_min = FloatProperty(name="min volume",
                                            description="Min volume selected.",
                                            min=0,
                                            default=0.)

bpy.types.Scene.sbv_reset_materials = BoolProperty(name="reset materials", description="reset materials", default=True)

bpy.types.Scene.inputfields = CollectionProperty(type=InputFieldGroup)
bpy.types.Scene.sbv_custom_materials = CollectionProperty(type=MaterialGroup)

bpy.types.Scene.sbv_colormaps = PointerProperty(type=ColormapGroup)
bpy.types.Scene.sbv_spacing_max = FloatProperty(name="Max Volume", min=0.00001, default=0.00001, description="spacing max volume")
bpy.types.Scene.sbv_spacing_min = FloatProperty(name="Min Volume", min=0.00001, default=0.00001, description="spacing min volume")
bpy.types.Scene.sbv_spacings = IntProperty(name="slices", min=0, default=1, description="slices")
bpy.types.Scene.sbv_logspace = BoolProperty(name="logspace", default=True)
bpy.types.Scene.sbv_id_string = StringProperty(name="id_string")
bpy.types.Scene.sbv_base_material_name = StringProperty()
