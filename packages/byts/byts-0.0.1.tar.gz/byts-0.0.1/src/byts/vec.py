"""
vec to int
"""

import numba
import numpy as np

@numba.njit()
def pack(l):
    s = 0
    for i, b in enumerate(l[::-1]):
        if b:
            s = s | (b << i)
    return s

@numba.njit()
def unpack(s):
    length = int(np.floor(np.log2(s))) + 1
    l = np.zeros(length, dtype=np.uint8)
    for i in range(length):
        if s & (1 << i):
            l[i] = 1
    return l[::-1]

@numba.njit()
def encode_standard_basis(u, n):
    l = np.zeros(n, dtype=np.uint8)
    for i in range(n):
        if u[i] > 0:
            l[i] = 1
    return l

@numba.njit()
def encode(u, n):
    l = encode_standard_basis(u, n)
    return pack(l)
