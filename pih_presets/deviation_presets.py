#!/usr/bin/env python3
"""
This module defines common functions to calculate the deviation between two hashes
"""
import numpy as np


def hamming_distance(array1, array2):
    if (array1.size != array2.size):
        raise Exception("Arrays have to have the same size")
    hamming = array1 != array2
    return np.count_nonzero(hamming) / hamming.size
