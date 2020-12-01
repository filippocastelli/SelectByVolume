import bpy
from bpy.types import Operator

from .multi_selection_op import ChunkSelectBase
from .material_applier import MaterialApplier
from .volume_selector import VolumeSelector
from .colors import hex_colors
from .property_groups import supported_colormaps

class MaterialOPBase():
    
    def _get_props(self, context):
        self.inputfield_list = context.scene.inputfields
        self.mesh_list = VolumeSelector.get_meshes()
        self.use_cached = context.scene.sbv_use_cached
        self.id_string = context.scene.sbv_id_string
        
    @staticmethod
    def _get_materials(context):
        inputfields = context.scene.inputfields
        materials = []
        for field in inputfields:
            materials.append(field.material)
        return materials
    
    @staticmethod
    def _set_colors(materials, colors):
        for idx, material in enumerate(materials):
            MaterialApplier.apply_color_to_material(material, colors[idx])
            
    @staticmethod
    def _get_selected_colors(context):
        selected_colors = []
        inputfields = context.scene.inputfields
        for field in inputfields:
            selected_colors.append(field.object_color)
        return selected_colors
    
    @staticmethod
    def _set_selected_colors(context, new_colors):
        inputfields = context.scene.inputfields
        for idx, field in enumerate(inputfields):
            field.object_color = new_colors[idx]


class ApplyAllMaterials_OT_Operator(Operator, MaterialOPBase):
    bl_idname = "view3d.applyallmaterialsop"
    bl_label = "Apply all Materials"
    bl_description = "Apply all Materials"

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
        return VolumeSelector.select_items(
            object_list=self.mesh_list,
            vol_min=vol_min,
            vol_max=vol_max,
            id_string=self.id_string,
            use_cached=self.use_cached,
            verbose=False)

class ApplyColormap_OT_Operator(Operator, MaterialOPBase):
    bl_idname = "view3d.applycolormap"
    bl_label = "Apply a ColorMap"
    bl_description = "Apply Colormap"

    def execute(self, context):
        print(context.scene.sbv_colormaps)
        materials = self._get_materials(context)
        control_colors = self._get_color_nodes(context)
        new_colors = MaterialApplier.apply_colormap_to_material_list(materials, control_colors, verbose=False)
        self._set_selected_colors(context, new_colors)
        return {"FINISHED"}
    
    @staticmethod
    def _get_color_nodes(context):
        colors = supported_colormaps[context.scene.sbv_colormaps.colormap]
        hex_color_nodes = []
        for color_name in colors:
            if "#" in color_name:
                hex_color_nodes.append(color_name)
            else:
                hex_color_nodes.append(hex_colors[color_name])
        return hex_color_nodes


class RandomizeColors_OT_Operator(Operator, MaterialOPBase):
    bl_idname = "view3d.randomizecolors"
    bl_label = "Apply Random Colors"
    bl_description = "Apply Random Colors"

    def execute(self, context):
        materials = self._get_materials(context)
        new_colors = []
        for material in materials:
            col_vars, _ = MaterialApplier.apply_rnd_color_to_material(material, verbose=False, return_color=True)
            new_colors.append(col_vars)
            self._set_selected_colors(context, new_colors)
        return {"FINISHED"}
    
    
class ApplySelectedColors_OT_Operator(Operator, MaterialOPBase):
    
    bl_idname = "view3d.applyselectedcolors"
    bl_label = "Apply Selected Colors"
    bl_description = "Apply Selected Colors"
    
    def execute(self, context):
        materials = self._get_materials(context)
        selected_colors = self._get_selected_colors(context)
        self._set_colors(materials, selected_colors)
        return {"FINISHED"}
    
