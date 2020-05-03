import bpy
from bpy.props import FloatProperty, PointerProperty, IntProperty, IntVectorProperty
from bpy.types import Material, PropertyGroup

class InputFieldGroup(PropertyGroup):
    id : IntProperty()
    threshold : FloatProperty(min=0.)
    material : PointerProperty(
        name = "Material",
        type = bpy.types.Material
    )

# THIS SHOULD KEEP TRACK OF ALL CREATED CUSTOM MATERIALS
class MaterialGroup(PropertyGroup):
    material : PointerProperty(
        name = "Material",
        type = bpy.types.Material
    )

    color : IntVectorProperty(
        size =3,
        name = "color",
        min = 0,
        max = 255
    )
    
    alpha : FloatProperty(
        min = 0.,
        max = 1)