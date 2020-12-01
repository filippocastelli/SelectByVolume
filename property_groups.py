import bpy
from bpy.props import FloatProperty, PointerProperty, IntProperty, IntVectorProperty, FloatVectorProperty
from bpy.types import Material, PropertyGroup

class InputFieldGroup(PropertyGroup):
    id : IntProperty()
    threshold : FloatProperty(min=0.)
    material : PointerProperty(
        name = "Material",
        type = bpy.types.Material
    )
    
    object_color : FloatVectorProperty(
        name = "object_color",
        subtype = "COLOR_GAMMA",
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = "if_color_picker"
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
    
    object_color = FloatVectorProperty(
        name = "object_color",
        subtype = "COLOR",
        default = (1.0, 1.0, 1.0),
        min = 0.0, max = 1.0,
        description = "color picker"
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
        ("5", "viridis", "viridis")
    ],
        description="colormap",
        default="0"
    )

viridis = ["#440154","#461768","#472C7A","#424085","#3B528B","#33638D","#2C738E","#26838F","#22928C","#2AA483","#56C068","#81D34D","#ABDC32","#D5E228","#FEE825"]
supported_colormaps = {
    "0" : ["yellow", "red"],
    "1" : ["yellow", "green", "blue", "violet"],
    "2" : ["blue", "red"],
    "3" : ["white", "black"],
    "4" : ["red", "green", "blue"],
    "5" : viridis
}

