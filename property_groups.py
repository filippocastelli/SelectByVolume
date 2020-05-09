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


class ColormapGroup(bpy.types.PropertyGroup):
    colormap : bpy.props.EnumProperty(
        items=[
        ("0", "yellow_red", "yellow_red"),
        ("1", "iridis", "iridis"),
        ("2", "blue_red", "blue_red"),
        ("3", "white_black", "white_black"),
        ("4", "rgb", "rgb"),
    ],
        description="colormap",
        default="0"
    )

supported_colormaps = {
    "0" : ["yellow", "red"],
    "1" : ["yellow", "green", "blue", "violet"],
    "2" : ["blue", "red"],
    "3" : ["white", "black"],
    "4" : ["red", "green", "blue"]
}