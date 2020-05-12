import bpy, bmesh
from mathutils import Color
from random import random
from itertools import accumulate, chain, repeat, tee
import numpy as np


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

def even_select(sequence, num):
    new_seq = []
    length = float(len(sequence))
    for i in range(num):
        new_seq.append(sequence[int(np.ceil(i * length / num))])
    return new_seq
    
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

