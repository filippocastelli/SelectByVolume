import bpy
from bpy.types import Operator
from bpy.props import IntProperty

from .utils import random_color, strictly_increasing, VolumeSelector, MaterialApplier
from .colors import hex_colors

# GLOBAL OPERATORS
class AddInputField_OT_Operator(Operator):
    bl_idname = "view3d.addinputfield"
    bl_label = "Create New Threshold"
    bl_description = "Create New Threshold"

    @staticmethod
    def _get_last_volume(inputfields):
        if len(inputfields) > 0:
            last_inputfield = inputfields[-1]
            return last_inputfield.threshold
        else:
            return 0.

    def _generate_field(self, context):
        current_field_n = len(context.scene.inputfields)
        current_volume = self._get_last_volume(context.scene.inputfields)
        newfield = context.scene.inputfields.add()
        newfield.id = current_field_n
        newfield.name = "Slice {}".format(current_field_n)
        newfield.threshold = current_volume

        self._generate_material(newfield, current_field_n, context)
        #print("Adding: now inputfields is {} long".format(len(context.scene.inputfields)))

    @staticmethod
    def _generate_material(input_field, current_field_n, context):
        material_name = "material_{}".format(current_field_n)

        try :
            assigned_material = context.scene.custom_materials[current_field_n].material
            input_field.material = assigned_material
        except IndexError:
            assigned_material = bpy.data.materials.new(name=material_name)
            col = random_color()
            rgb_color = (col.r, col.g, col.b)
            alpha = 1.0
            MaterialApplier.apply_color_to_material(assigned_material, rgb_color, alpha)
            input_field.material = assigned_material
            input_field.color = rgb_color
            input_field.alpha = alpha
            new_custom_material = context.scene.custom_materials.add()
            new_custom_material.material = assigned_material

    def execute(self, context):
        self._generate_field(context)
        return {"FINISHED"}

class RemoveInputField_OT_Operator(Operator):
    bl_idname = "view3d.removeinputfield"
    bl_label = "Remove Threshold"
    bl_description = "Remove Threshold"

    def _remove_field(self, context):
        current_field_n = len(context.scene.inputfields)
        context.scene.inputfields.remove(current_field_n -1)
        #print("Removing: now inputfields is {} long".format(len(context.scene.inputfields)))

    def execute(self, context):
        self._remove_field(context)
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        current_field_n = len(context.scene.inputfields)
        return current_field_n > 0

class ResetFields_OT_Operator(Operator):

    bl_idname = "view3d.resetfields"
    bl_label = "Reset Volume Slices"
    bl_description = "Reset Input Field (description)"

    def _reset_field(self, context):
        context.scene.inputfields.clear()
        if context.scene.sbv_reset_materials:
            self._reset_materials(context)
            #print("Resetting Materials...")
            #print("Resetting: now inputfields is {} long, materials is {} long".format(len(context.scene.inputfields),
            #                                                                    len(context.scene.custom_materials)))

    def execute(self, context):
        self._reset_field(context)
        return {"FINISHED"}
    
    def _reset_materials(self, context):
        for material_elem in context.scene.custom_materials:
            mat = material_elem.material
            bpy.data.materials.remove(mat)
        context.scene.custom_materials.clear()


# SECTION OPERATORS
class ChunkSelectBase:
    """Base class for chunk-selection based buttons"""
    def execute(self, context):
        self.get_props(context)
        #print("Pressed button ", self.id, self.inputfield.name)
        bpy.ops.object.select_all(action='DESELECT')
        self.selected_items = VolumeSelector.select_items(self.mesh_list, self.vol_min, self.vol_max, use_cached=self.use_cached, verbose=False)
        return {'FINISHED'}

    def get_props(self, context):
        self.inputfield = context.scene.inputfields[self.id]
        self.vol_min, self.vol_max = self.get_volume_bounds(context, self.id)
        self.use_cached = context.scene.sbv_use_cached
        self.mesh_list = VolumeSelector.get_meshes()
        self.material = self.inputfield.material

    def invoke(self, context, event):
        return self.execute(context)

    @staticmethod
    def get_volume_bounds(context, id):
        vol_min = context.scene.inputfields[id -1].threshold if id > 0 else 0.
        vol_max = context.scene.inputfields[id].threshold
        return vol_min, vol_max

    @classmethod
    def poll(cls, context):
        threshold_list = [inputfield.threshold for inputfield in context.scene.inputfields]
        return strictly_increasing(threshold_list)


class SelectChunk_OT_Operator(Operator, ChunkSelectBase):
    """SelectChunk #i button"""
    bl_idname = "view3d.selectchunkop"
    bl_label = "Select Chunk"
    bl_description = "Select Chunk"

    id : IntProperty()


class ApplyMaterials_OT_Operator(Operator, ChunkSelectBase):
    """ApplyMaterial #i Button"""
    bl_idname = "view3d.applymaterialsop"
    bl_label = "Apply Materials to Chunk"
    bl_description = "Apply Materials to Chunk"

    id : IntProperty()
    
    def execute(self, context):
        super().execute(context)
        MaterialApplier.apply_material(self.selected_items, self.material)
        return {"FINISHED"}


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
        materials = self._get_materials(context)
        control_colors = self._get_colors(context)
        MaterialApplier.apply_colormap_to_material_list(materials, control_colors)
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
        color_0 = hex_colors["blue"]
        color_1 = hex_colors["red"]

        return [color_0, color_1]