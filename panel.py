import bpy
import numpy as np

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
    @staticmethod
    def get_volume_stats(context):
        if len(context.selected_objects) == 0 or "sbv_volume" not in context.selected_objects[0]:
            vol_min = -1
            vol_max = -1
            vol_mean = -1
            vol_std = -1
            vol_median = -1
            vol_len = 0
        
        else:
            volumes = [object["sbv_volume"] for object in context.selected_objects]
            vol_len = len(volumes)
            vol_min = np.min(volumes)
            vol_max = np.max(volumes)
            vol_mean = np.mean(volumes)
            vol_median = np.median(volumes)
            vol_std = np.std(volumes)

        return {
            "len" : vol_len,
            "min" : vol_min,
            "max": vol_max,
            "mean": vol_mean,
            "median": vol_median,
            "std": vol_std
            }

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"

        flags_box = layout.box()

        flags_box.label(text="global options")
        flags_box.row().prop(context.scene, "sbv_use_multithread")
        flags_box.row().prop(context.scene, "sbv_use_cached") 
        id_string_row = flags_box.row() 
        id_string_row.prop(context.scene, "sbv_id_string")

        info_box = layout.box()
        info_box.label(text="selection info")
        object_name, object_volume = self.get_volume_details(context)
        info_box.row().label(text="selected object: {}".format(object_name))
        info_box.row().label(text = "volume: {}".format(object_volume))
        vol_stats = self.get_volume_stats(context)

        info_box.row().label(text = "stats: # of obj: {}, min: {:.2f}, max: {:.2f}".format(
            vol_stats["len"],
            vol_stats["min"],
            vol_stats["max"],
        ) )

        info_box.row().label(text = "mean: {:.2f}, median: {:.2f}, std: {:.2f}".format(
            vol_stats["mean"],
            vol_stats["median"],
            vol_stats["std"]
        ) )

        simple_selection_box = layout.box()
        simple_selection_box.label(text="simple range selection")

        #simple_selection_box.enabled = self._is_inputfield_enabled(context)
        
        min_max_row = simple_selection_box.row()
        min_max_row.prop(context.scene, "sbv_vol_min")
        min_max_row.prop(context.scene, "sbv_vol_max")
        simple_selection_box.row().operator("view3d.selectbyvolumeop", text="Select By Volume")

        multiple_selection_box = layout.box()
        multiple_selection_box.label(text="multiple range selection")

        for i, field in enumerate(context.scene.inputfields):
            sub_box = multiple_selection_box.box()
            sub_box.label(text=field.name)
            mat  = field.material
            sub_box.row().prop(field, "threshold", text="vol. threshold")
            button_row = sub_box.row()
            button_row.prop(mat, "name", text="", emboss=False, icon_value=layout.icon(mat))
            button_row.operator("view3d.selectchunkop", text="SELECT").id = i
            button_row.operator("view3d.applymaterialsop", text="APPLY MAT.").id = i

        add_remove_row = multiple_selection_box.row()
        add_remove_row.operator("view3d.addinputfield", text="Add Threshold")
        add_remove_row.operator("view3d.removeinputfield", text="Remove Threshold")
        reset_row = multiple_selection_box.row()
        reset_row.prop(context.scene, "sbv_reset_materials")
        reset_row.operator("view3d.resetfields", text="Reset Thresholds")
        spaced_gen_settings_row = multiple_selection_box.row()
        spaced_gen_settings_row.prop(context.scene, "sbv_spacing_min")
        spaced_gen_settings_row.prop(context.scene, "sbv_spacing_max")
        spaced_gen_settings_row.prop(context.scene, "sbv_spacings")
        gen_spaced_row = multiple_selection_box.row()
        gen_spaced_row.prop(context.scene,"sbv_logspace")
        gen_spaced_row.operator("view3d.generatespaced", text="Lin/Log Spaced Selections")
        
        materials_box = layout.box()
        materials_box.label(text="materials")
        materials_box.row().prop_search(context.scene, "sbv_base_material_name", bpy.data, "materials", text="base material")
        apply_all_materials_row = materials_box.row()
        apply_all_materials_row.operator("view3d.applyallmaterialsop", text="Apply Materials To All Selections")


        apply_colormap_row = materials_box.row()
        apply_colormap_row.operator("view3d.applycolormap", text="Apply Colormap")
        apply_colormap_row.prop(context.scene.sbv_colormaps, "colormap")

        randomize_colors_row = materials_box.row()
        randomize_colors_row.operator("view3d.randomizecolors", text="Randomize Colors")
