"""
This module defines common perceptual image hashing algorithms that can be used as an example
"""
import numpy
import cv2
from scipy import fftpack as fft


"""
Average Hash - AHash
"""


def aHash(image, hash_size=8):

    if hash_size < 0:
        raise ValueError("Hash size must be positive")

    # reduce size and complexity, then covert to grayscale
    image = cv2.resize(image, (hash_size, hash_size),
                       interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # find average pixel value
    avg = gray.mean()
    # create string of bits
    diff = gray > avg
    # make a hash
    return diff.flatten()


#------------------------------------------------------------------------------#
"""
Difference Hash - DHash
"""


def dHash(image, hash_size=8):

    if hash_size < 0:
        raise ValueError("Hash size must be positive")

    image = cv2.resize(image, (hash_size+1, hash_size),
                       interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # compute differences between columns
    diff = gray[:, 1:] > gray[:, :-1]
    return diff.flatten()


#------------------------------------------------------------------------------#
"""
PHash
"""


def pHash(image, dSize=8, dFactor=4):
    image = cv2.resize(image, (dSize*dFactor, dSize*dFactor),
                       interpolation=cv2.INTER_AREA)
    gray = ip.convert_image_to_grayscale(image)

    # DCT berechnen
    p_dct = fft.dct(gray)

    # compute average of low frequencies
    p_dct_low = np.array(p_dct[: dSize, 1:dSize+1])
    # p_dct_low[0,0]=0
    p_avg = p_dct_low.mean()

    p_dif = p_dct_low > p_avg

    return p_dif.flatten()
