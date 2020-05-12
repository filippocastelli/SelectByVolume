
import bpy, bmesh

class VolumeSelector():
    @staticmethod
    def get_volume(object, verbose = False, use_cached=False):
        if ("sbv_volume" in object) and (use_cached):
            volume = object["sbv_volume"]
        else:
            bm = bmesh.new()
            bm.from_mesh(object.data)
            
            volume = float(bm.calc_volume())
            object["sbv_volume"] = volume
        
        if verbose:
            print("Object {} has volume {}".format(object.name, volume))
        return volume
    
    @classmethod
    def select_items(cls, object_list, vol_min, vol_max, id_string=None, use_cached=False, verbose=False):
        selected_items = []
        first_active = False
        for object in object_list:
            volume = cls.get_volume(object, use_cached=use_cached, verbose=verbose)
            is_neuron = id_string in object.name if id_string else True
            if volume > vol_min and volume < vol_max and is_neuron:
                if not first_active:
                    bpy.context.view_layer.objects.active = object
                    first_active = True
                selected_items.append(object)
                object.select_set(state=True)
            #else:    # too slow
            #    object.select_set(state=False)
        return selected_items

    @staticmethod
    def get_meshes():
        return [mesh for mesh in bpy.context.scene.objects if mesh.type == "MESH"]