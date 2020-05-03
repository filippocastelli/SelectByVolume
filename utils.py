import bpy, bmesh
from mathutils import Color
from random import random
from itertools import accumulate, chain, repeat, tee
import numpy as np

from .colors import rgb_colors, hex_colors
from .colormap import polylinear_gradient, linear_gradient, hex_to_RGB

def random_color():
    return Color((random(), random(), random()))

def split_chunks(xs, n):
    assert n > 0
    L = len(xs)
    s, r = divmod(L, n)
    widths = chain(repeat(s+1, r), repeat(s, n-r))
    offsets = accumulate(chain((0,), widths))
    b, e = tee(offsets)
    next(e)
    return [xs[s] for s in map(slice, b, e)]
    
def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))

def monotonic(L):
    return non_increasing(L) or non_decreasing(L)


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
    def select_items(cls, object_list, vol_min, vol_max, use_cached=False, verbose=False):
        selected_items = []
        first_active = False
        for object in object_list:
            volume = cls.get_volume(object, use_cached=use_cached, verbose=verbose)
            if volume > vol_min and volume < vol_max:
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

class MaterialApplier():
    @classmethod
    def apply_material(cls, object_list, material, use_loop = False):
        """use_loop == False requires objects to be selected, and at least one object to be active"""
        if use_loop:
            for object in object_list:
                cls._material_write(object, material)
        else:
            cls._material_write(object_list[0], material)
            bpy.ops.object.make_links_data(type="MATERIAL")


    @staticmethod
    def _material_write(object, material):
        if object.data.materials:
            object.data.materials[0] = material
        else:
            object.data.materials.append(material)


    @staticmethod
    def gen_colormap(hex_colors, n_steps):
        "takes list of hex colors, returns polylinear gradient interpolated colors in RGB format"
        return polylinear_gradient(hex_colors, n_steps)
    
    @classmethod
    def apply_colormap_to_material_list(cls, material_list, hex_colors):
        n_steps = len(material_list)
        colormap = cls.gen_colormap(hex_colors, n_steps)
        assert len(colormap) == n_steps, "Wrong colormap dimension"

        for i, material in enumerate(material_list):
            cls.apply_color_to_material(material, colormap[i], alpha=1.0)

    @staticmethod
    def hextorgb(hex_color):
        return hex_to_RGB(hex_color)

    @staticmethod
    def apply_color_to_material(material, rgb_color, alpha=1.0):
        material.diffuse_color = (*rgb_color, alpha)