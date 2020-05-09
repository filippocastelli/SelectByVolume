import bpy
from bpy.types import Operator

from .multi_selection_op import ChunkSelectBase
from .utils import VolumeSelector, MaterialApplier
from .colors import hex_colors
from .property_groups import supported_colormaps

class ApplyAllMaterials_OT_Operator(Operator):
    bl_idname = "view3d.applyallmaterialsop"
    bl_label = "Apply all Materials"
    bl_description = "Apply all Materials"

    def _get_props(self, context):
        self.inputfield_list = context.scene.inputfields
        self.mesh_list = VolumeSelector.get_meshes()
        self.use_cached = context.scene.sbv_use_cached

    def execute(self, context):
        self._get_props(context)
        for i, inputfield in enumerate(self.inputfield_list):
            vol_min, vol_max = ChunkSelectBase.get_volume_bounds(context, i)
            material = inputfield.material
            selected_items = self._select_range(vol_min, vol_max)
            if len(selected_items) > 0:
                MaterialApplier.apply_material(selected_items, material)
        bpy.ops.object.select_all(action='DESELECT')

        return {"FINISHED"}

    def _select_range(self, vol_min, vol_max):
        bpy.ops.object.select_all(action='DESELECT')
        return VolumeSelector.select_items(self.mesh_list, vol_min, vol_max, use_cached=self.use_cached, verbose=False)

    @staticmethod
    def _get_materials(context):
        inputfields = context.scene.inputfields
        materials = []
        for field in inputfields:
            materials.append(field.material)
        return materials
    
    @staticmethod
    def _get_colors(context):
        color_0 = hex_colors["blue"]
        color_1 = hex_colors["red"]

        return [color_0, color_1]

class ApplyColormap_OT_Operator(Operator):
    bl_idname = "view3d.applycolormap"
    bl_label = "Apply a ColorMap"
    bl_description = "Apply Colormap"

    def execute(self, context):
        print(context.scene.sbv_colormaps)
        materials = self._get_materials(context)
        control_colors = self._get_colors(context)
        MaterialApplier.apply_colormap_to_material_list(materials, control_colors, verbose=False)
        return {"FINISHED"}

    @staticmethod
    def _get_materials(context):
        inputfields = context.scene.inputfields
        materials = []
        for field in inputfields:
            materials.append(field.material)
        return materials
    
    @staticmethod
    def _get_colors(context):
        colors = supported_colormaps[context.scene.sbv_colormaps.colormap]

        hex_color_nodes = [hex_colors[color_name] for color_name in colors]
        return hex_color_nodes


class RandomizeColors_OT_Operator(Operator):
    bl_idname = "view3d.randomizecolors"
    bl_label = "Apply Random Colors"
    bl_description = "Apply Random Colors"

    def execute(self, context):
        materials = self._get_materials(context)
        for material in materials:
            MaterialApplier.apply_rnd_color_to_material(material, verbose=False)
        return {"FINISHED"}

    @staticmethod
    def _get_materials(context):
        inputfields = context.scene.inputfields
        materials = []
        for field in inputfields:
            materials.append(field.material)
        return materials