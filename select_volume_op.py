import bpy, bmesh
from bpy.props import FloatProperty, BoolProperty, PointerProperty, IntProperty
from bpy.types import Operator
import threading, multiprocessing

from .utils import split_chunks
from .volume_selector import VolumeSelector

class SelectByVolume_OT_Operator(Operator):
    """Select by Volume Button simple selection"""
    bl_idname = "view3d.selectbyvolumeop"
    bl_label = "Select By Volume Operator"
    bl_description = "Select by volume"

    def get_props(self, context):
        self.multithread = context.scene.sbv_use_multithread
        self.use_cached = context.scene.sbv_use_cached
        self.vol_max = context.scene.sbv_vol_max
        self.vol_min = context.scene.sbv_vol_min
        self.id_string = context.scene.sbv_id_string

    def execute(self, context):
        #deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        self.get_props(context)
        scene_meshes = VolumeSelector.get_meshes()

        if self.multithread:
            print("Using multithreaded mode")
            scene_meshes_chunks = list(split_chunks(scene_meshes, multiprocessing.cpu_count()))
            threads = [threading.Thread(target=VolumeSelector.select_items, args=(obj_list, self.vol_min, self.vol_max, self.id_string, self.use_cached)) for obj_list in scene_meshes_chunks]
            
            for i, thread in enumerate(threads):
                # print("Starting thread {} / {}".format(i, len(threads)))
                thread.start()
            for j, thread in enumerate(threads):
                # print("Joining thread {} / {}".format(j, len(threads)))
                thread.join()
        else:
            print("Using single-threaded mode")
            VolumeSelector.select_items(object_list=scene_meshes,
                                        vol_min=self.vol_min,
                                        vol_max=self.vol_max,
                                        id_string=self.id_string,
                                        use_cached=self.use_cached)

        return {"FINISHED"}
    
    @classmethod
    def poll(cls , context):
        ordered = context.scene.sbv_vol_min < context.scene.sbv_vol_max
        non_negative = (context.scene.sbv_vol_min >= 0) and (context.scene.sbv_vol_max > 0)
        
        return ordered and non_negative

