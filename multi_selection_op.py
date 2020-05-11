import bpy
import numpy as np

from bpy.types import Operator
from bpy.props import IntProperty

from .utils import strictly_increasing, VolumeSelector, MaterialApplier

class InputFieldManager():
    @staticmethod
    def get_last_volume(context):
        inputfields = context.scene.inputfields
        if len(inputfields) > 0:
            last_inputfield = inputfields[-1]
            return last_inputfield.threshold
        else:
            return 0.
        
    @classmethod
    def add_field(cls, context, volume=None):
        inputfields = context.scene.inputfields
        current_field_n = len(context.scene.inputfields)
        new_volume = volume if volume is not None else cls.get_last_volume(context)
        newfield = context.scene.inputfields.add()

        newfield.name =  "Slice {}".format(current_field_n)
        newfield.threshold = new_volume
        cls.generate_material(newfield, current_field_n, context)
    
    @classmethod
    def remove_field(cls, context):
        current_field_n = len(context.scene.inputfields)
        context.scene.inputfields.remove(current_field_n -1)

    @staticmethod
    def generate_material(input_field, current_field_n, context):
        material_name = "material_{}".format(current_field_n)

        try :
            assigned_material = context.scene.custom_materials[current_field_n].material
            input_field.material = assigned_material
        except IndexError:
            assigned_material = bpy.data.materials.new(name=material_name)
            color_vals, alpha = MaterialApplier.apply_rnd_color_to_material(assigned_material, return_color=True)
            input_field.material = assigned_material
            input_field.color = color_vals
            input_field.alpha = alpha
            new_custom_material = context.scene.custom_materials.add()
            new_custom_material.material = assigned_material
    
    @classmethod
    def add_multiple_fields(cls, context, volumes):
        for volume in volumes:
            cls.add_field(context, volume=volume)



# GLOBAL OPERATORS
class AddInputField_OT_Operator(Operator):
    bl_idname = "view3d.addinputfield"
    bl_label = "Create New Threshold"
    bl_description = "Create New Threshold"

    def execute(self, context):
        InputFieldManager.add_field(context)
        return {"FINISHED"}

class RemoveInputField_OT_Operator(Operator):
    bl_idname = "view3d.removeinputfield"
    bl_label = "Remove Threshold"
    bl_description = "Remove Threshold"

    def execute(self, context):
        InputFieldManager.remove_field(context)
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

class GenerateSpaced_OT_Operator(Operator):

    bl_idname = "view3d.generatespaced"
    bl_label = "Generate Multiple Selections"
    bl_description = "Generate Multiple Selections"

    def _get_props(self, context):
        self.max_volume = context.scene.sbv_spacing_max
        self.min_volume = context.scene.sbv_spacing_min
        self.spacings = context.scene.sbv_spacings
        self.logspace = context.scene.sbv_logspace

    def execute(self, context):
        self._get_props(context)
        bpy.ops.view3d.resetfields()
        if self.logspace:
            inputfield_values = np.geomspace(start=self.min_volume, stop=self.max_volume, num=self.spacings +1)[1:]
        else:
            inputfield_values = np.linspace(start=self.min_volume, stop=self.max_volume, num=self.spacings +1)[1:]
        InputFieldManager.add_multiple_fields(context, inputfield_values)
        return {"FINISHED"}

# SECTION OPERATORS
class ChunkSelectBase:
    """Base class for chunk-selection based buttons"""
    def execute(self, context):
        self.get_props(context)
        #print("Pressed button ", self.id, self.inputfield.name)
        bpy.ops.object.select_all(action='DESELECT')
        self.selected_items = VolumeSelector.select_items(object_list=self.mesh_list,
                                                        vol_min=self.vol_min,
                                                        vol_max=self.vol_max,
                                                        id_string=self.id_string,
                                                        use_cached=self.use_cached,
                                                        verbose=False)
        return {'FINISHED'}

    def get_props(self, context):
        self.inputfield = context.scene.inputfields[self.id]
        self.vol_min, self.vol_max = self.get_volume_bounds(context, self.id)
        self.use_cached = context.scene.sbv_use_cached
        self.mesh_list = VolumeSelector.get_meshes()
        self.material = self.inputfield.material
        self.id_string = context.scene.sbv_id_string

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

