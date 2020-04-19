import bpy


class SelectByVolume_PT_Panel(bpy.types.Panel):
    bl_idname = "SBV_PT_panel"
    bl_label = "Select Objects by Volume"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.row().prop(context.scene, "sbv_use_multithread")
        layout.row().prop(context.scene, "sbv_use_cached")
        layout.row().prop(context.scene, "sbv_vol_min")
        layout.row().prop(context.scene, "sbv_vol_max")
        layout.row().operator("view3d.selectbyvolumeop", text="Select by volume")