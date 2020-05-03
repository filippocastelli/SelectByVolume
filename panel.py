import bpy

class SelectByVolume_PT_Panel(bpy.types.Panel):
    bl_idname = "SBV_PT_panel"
    bl_label = "Select Objects by Volume"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def _is_inputfield_enabled(self, context):
        try :
            len_inputfield = len(context.scene.inputfields)
        except AttributeError:
            len_inputfield = 0
        return not len_inputfield > 0

    @staticmethod
    def get_volume_details(context):
        if len(context.selected_objects) == 0:
            return "none", "select something first"

        selected_object = context.selected_objects[0]
        name = selected_object.name

        try:
            volume = selected_object["sbv_volume"]
            volume = "{:.3f}".format(volume)
        except KeyError:
            return name, "undefined, run a volume selection without caching first"
        
        return name, volume

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"

        flags_box = layout.box()

        flags_box.label(text="global options")
        flags_box.row().prop(context.scene, "sbv_use_multithread")
        flags_box.row().prop(context.scene, "sbv_use_cached") 

        info_box = layout.box()
        info_box.label(text="selection info")
        object_name, object_volume = self.get_volume_details(context)
        info_box.row().label(text="selected object: {}".format(object_name))
        info_box.row().label(text = "volume: {}".format(object_volume))

        simple_selection_box = layout.box()
        simple_selection_box.label(text="simple range selection")

        #simple_selection_box.enabled = self._is_inputfield_enabled(context)
        
        min_max_row = simple_selection_box.row()
        min_max_row.prop(context.scene, "sbv_vol_min")
        min_max_row.prop(context.scene, "sbv_vol_max")
        simple_selection_box.row().operator("view3d.selectbyvolumeop", text="Select By Volume")

        multiple_selection_box = layout.box()
        multiple_selection_box.label(text="multiple range selection")
        add_remove_row = multiple_selection_box.row()
        reset_row = multiple_selection_box.row()
        #apply_colormap_row = multiple_selection_box.row()
        apply_all_materials_row = multiple_selection_box.row()
        
        add_remove_row.operator("view3d.addinputfield", text="Add Threshold")
        add_remove_row.operator("view3d.removeinputfield", text="Remove Threshold")
        reset_row.prop(context.scene, "sbv_reset_materials")
        reset_row.operator("view3d.resetfields", text="Reset Thresholds")
        #apply_colormap_row.operator("view3d.applycolormap", text="ApplyColorMap")ù
        apply_all_materials_row.operator("view3d.applyallmaterialsop", text="Apply Materials To All Selections")

        #multiple_selection_box.row().prop_search(context.scene, "theChosenObject", bpy.data, "materials", text="base material")

        for field in context.scene.inputfields:
            sub_box = multiple_selection_box.box()
            sub_box.label(text=field.name)
            mat  = field.material
            sub_box.row().prop(field, "threshold", text="vol. threshold")
            button_row = sub_box.row()
            button_row.prop(mat, "name", text="", emboss=False, icon_value=layout.icon(mat))
            button_row.operator("view3d.selectchunkop", text="SELECT").id = field.id
            button_row.operator("view3d.applymaterialsop", text="APPLY MAT.").id = field.id