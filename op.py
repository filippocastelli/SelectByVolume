import bpy, bmesh
from bpy.props import FloatProperty, BoolProperty, PointerProperty

import threading, multiprocessing

from .split_chunks import split_chunks

class SelectByVolume_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.selectbyvolumeop"
    bl_label = "Select By Volume Operator"
    bl_description = "Select by volume"

    def get_props(self, context):
        self.multithread = context.scene.sbv_use_multithread
        self.use_cached = context.scene.sbv_use_cached
        self.vol_max = context.scene.sbv_vol_max
        self.vol_min = context.scene.sbv_vol_min
        
    def get_volume(self, object, verbose = False):
        
        if ("sbv_volume" in object) and (self.use_cached):
            volume = object["sbv_volume"]
        else:
            bm = bmesh.new()
            bm.from_mesh(object.data)
            
            volume = float(bm.calc_volume())
            object["sbv_volume"] = volume
        
        if verbose:
            print("Object {} has volume {}".format(object.name, volume))
        return volume

    def select_items(self, object_list, vol_min, vol_max):
        for object in object_list:
            volume = self.get_volume(object, verbose = False)
            if volume > vol_min and volume < vol_max:
                object.select_set(state=True)
            #else:    # too slow
            #    object.select_set(state=False)

    def get_meshes(self):
        return [mesh for mesh in bpy.context.scene.objects if mesh.type == "MESH"]
    
    def execute(self, context):
        #deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        self.get_props(context)
        scene_meshes = self.get_meshes()

        if self.multithread:
            print("Using multithreaded mode")
            scene_meshes_chunks = list(split_chunks(scene_meshes, multiprocessing.cpu_count()))
            threads = [threading.Thread(target=self.select_items, args=(obj_list, self.vol_min, self.vol_max)) for obj_list in scene_meshes_chunks]
            
            for i, thread in enumerate(threads):
                # print("Starting thread {} / {}".format(i, len(threads)))
                thread.start()
            for j, thread in enumerate(threads):
                # print("Joining thread {} / {}".format(j, len(threads)))
                thread.join()
        else:
            print("Using single-threaded mode")
            self.select_items(scene_meshes, self.vol_min, self.vol_max)

        return {"FINISHED"}
    
    @classmethod
    def poll(cls , context):
        ordered = context.scene.sbv_vol_min < context.scene.sbv_vol_max
        non_negative = (context.scene.sbv_vol_min >= 0) and (context.scene.sbv_vol_max > 0)
        
        return ordered and non_negative