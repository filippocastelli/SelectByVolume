import bpy
from .material_applier import MaterialApplier

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
            assigned_material = context.scene.sbv_custom_materials[current_field_n].material
            input_field.material = assigned_material
        except IndexError:
            base_material_name = context.scene.sbv_base_material_name
            if base_material_name != "":
                assigned_material = bpy.data.materials[base_material_name].copy()
                assigned_material.name = material_name
            else:
                assigned_material = bpy.data.materials.new(name=material_name)
                assigned_material.use_nodes = True
            
            color_vals, alpha = MaterialApplier.apply_rnd_color_to_material(assigned_material, return_color=True)
            input_field.material = assigned_material
            input_field.color = color_vals
            input_field.object_color = color_vals
            input_field.alpha = alpha
            new_custom_material = context.scene.sbv_custom_materials.add()
            new_custom_material.material = assigned_material
            new_custom_material.object_color = color_vals
    
    @classmethod
    def add_multiple_fields(cls, context, volumes):
        for volume in volumes:
            cls.add_field(context, volume=volume)