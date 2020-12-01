import bpy
from .utils import random_color

from .colors import rgb_colors, hex_colors
from .colormap import polylinear_gradient, linear_gradient, hex_to_RGB

class MaterialApplier():
    @classmethod
    def apply_material(cls, object_list, material, use_loop = False):
        """apply material to an object list
        can either assign a material to every element in a list (disabled by default)
        because it's slow af, or make material links between every selected object
        objects need to be selected first.

        Parameters
        ----------
        object_list : tuple
            tuple of objects
        material : bpy.types.Material
            material to apply to a list of objects
        use_loop : bool, optional
            if true loops over every object in list and assigns material elementwise, by default False
        """
        if len(object_list) > 0:
            if use_loop:
                for object in object_list:
                    cls._material_write(object, material)
            else:
                cls._material_write(object_list[0], material)
                bpy.ops.object.make_links_data(type="MATERIAL")
        else:
            pass

    @staticmethod
    def _material_write(object, material):
        """write material to first material slot in object"""
        if object.data.materials:
            if object.data.materials[0] != material:
                object.data.materials[0] = material
        else:
            object.data.materials.append(material)

    @classmethod
    def gen_colormap(cls, hex_colors, n_steps):
        "takes list of hex colors, returns polylinear gradient interpolated colors in RGB format"
        rgb_8bit_values = polylinear_gradient(hex_colors, n_steps)
        return cls.normalize_color_list(rgb_8bit_values)

    @staticmethod
    def normalize_color(color):
        """converts a single (r,g,b) color in [0, 255] to [0,1] format"""
        normalized = []
        for channel in color:
            normalized.append(channel/255)
        return normalized
    
    @classmethod
    def normalize_color_list(cls, color_list):
        """converts a list of (r,g,b) [0,25] colors to [0,1] format"""
        normalized_list = []

        for color in color_list:
            normalized_list.append(cls.normalize_color(color))

        return normalized_list
    
    @classmethod
    def apply_colormap_to_material_list(cls, material_list, hex_colors, verbose=False):
        """apply colormap to a list of materials

        Parameters
        ----------
        material_list : list
            list of bpy.types.Material materials
        hex_colors : list
            list of node colors in hex format, colormap will be an interpolation of these colors
        verbose : bool, optional
            verbose mode, by default False
        """
        n_steps = len(material_list)
        colormap = cls.gen_colormap(hex_colors, n_steps)
        assert len(colormap) == n_steps, "Wrong colormap dimension"

        for i, material in enumerate(material_list):
            cls.apply_color_to_material(material, colormap[i], alpha=1.0, verbose=verbose)

        return colormap
        
    @staticmethod
    def hextorgba(hex_color):
        """convert hex color to rgba tuple"""
        return hex_to_RGB(hex_color)
    
    @staticmethod
    def apply_color_to_material(material, color, alpha=1.0, verbose=False):
        """apply color to material

        Parameters
        ----------
        material : bpy.types.Material
            blender material to apply color on
        rgb_color : tuple
            (r,g,b) color tuple, colors are normalized in [0,1]
        alpha : float, optional
            alpha value, by default 1.0
        verbose : bool, optional
            verbose mode, by default False
        """
        
        if verbose:
            print("Applying color {} to material {}".format(color, material.name))
        material.diffuse_color = (*color, alpha)
        try: #if material has a Principled BSDF node set its Base Color
            material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*color, alpha)
        except (IndexError, AttributeError):
            pass

    @classmethod
    def apply_rnd_color_to_material(cls, material, return_color=False, verbose=False):
        """apply random color to material

        Parameters
        ----------
        material : bpy.types.Material
            material to apply color on
        return_color : bool, optional
            if True returns (r,g,b,alpha) color tuple, by default False
        verbose : bool, optional
            verbose mode, by default False

        Returns
        -------
        tuple
            (r,g,b,alpha) color tuple
        """
        color = random_color()
        color_vals = (color.r, color.g, color.b)
        alpha = 1.0
        cls.apply_color_to_material(material, color_vals, verbose=verbose)

        if return_color:
            return color_vals, alpha