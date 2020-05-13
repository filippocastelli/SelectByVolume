import numpy as np
from numpy import random as rnd
from .utils import even_select


def hex_to_RGB(hex):
    """ "#FFFFFF" -> [255,255,255] """
    # Pass 16 to the integer function for change of base
    return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    """ [255,255,255] -> "#FFFFFF" """
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#" + "".join(
        ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB]
    )


def color_dict(gradient):
    """ Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on """
    return {
        "hex": [RGB_to_hex(RGB) for RGB in gradient],
        "r": [RGB[0] for RGB in gradient],
        "g": [RGB[1] for RGB in gradient],
        "b": [RGB[2] for RGB in gradient],
    }


def rand_hex_color(num=1):
    """ Generate random hex colors, default is one,
      returning a string. If num is greater than
      1, an array of strings is returned. """
    colors = [RGB_to_hex([x * 255 for x in rnd.rand(3)]) for i in range(num)]
    if num == 1:
        return colors[0]
    else:
        return colors


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """ returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") """
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
        
    return RGB_list


def polylinear_gradient(colors, n):
    """ returns a list of colors forming linear gradients between
      all sequential pairs of colors. "n" specifies the total
      number of desired output colors """
    # The number of colors per individual linear gradient
    altmode = (n < len(colors) -1)

    steps_per_gradient = n // (len(colors) -1) if not altmode else 1
    remainder_steps = n % (len(colors) -1) if not altmode else 0
    
    gradient_list = []
    if len(colors) == 1:
        # if we have just one color we make a transition to white (? maybe it's dumb)
        colors.append("#FFFFFF")
    if len(colors) == 2:
        # if we have two colors we just make a linear gradient
        gradient_list = linear_gradient(colors[0], colors[1], n)
    else:
        # else we calculate a polylinear gradient
        for i, color in enumerate(colors[:-1]):
            if i < len(colors) -2:
                gradient_list += linear_gradient(colors[i], colors[i+1], steps_per_gradient + 1)[0:-1]
            else:
                gradient_list += linear_gradient(colors[i], colors[i+1], steps_per_gradient + remainder_steps +1)[1:]
    
    if altmode:
        # if we have more node colors than sampling steps
        # we have calculated a polylinear gradient with step 1 between all nodes
        # we select n elements from this list 
        gradient_list = even_select(gradient_list, n)
    return gradient_list   


def colordict2tcolors(colordict):
    r_c = colordict["r"]
    g_c = colordict["g"]
    b_c = colordict["b"]

    zipped_cols = zip(r_c, g_c, b_c)
    return list(zipped_cols)
