import numpy as np
from pih_presets.utils import load_image
from pih_presets.deviation_presets import hamming_distance
from pih_presets.hashalgos_preset import dHash, aHash, pHash

"""Wrapper for aHash"""


def test_aHash(aOriginalImages, aComparativeImages, lThreshold=0.2, lHashSize=16, oCache=None):

    # create dictionary of metadata
    dicMetadata = {"algorithm": "aHash",
                   "hash_size": lHashSize, "threshold": lThreshold}

    # compare every image
    aDecisions = []
    for i, sOriginalImagePath in enumerate(aOriginalImages):
        sComparativeImagePath = aComparativeImages[i]

        if oCache:
            # create unique cache key for original and comparative key
            aCacheKeyBase = ["aHash", lHashSize]
            sOriginalImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sOriginalImagePath)
            sComparativeImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sComparativeImagePath)

            # check for existence of keys in cache
            aHashOriginal = oCache.get(sOriginalImageCacheKey)
            aHashComparative = oCache.get(sComparativeImageCacheKey)

        # get images from path and calculate hash if not in hash already
        # add to cache if calculated the first time and cache is active
        if aHashOriginal is None:
            aOriginalImage = load_image(sOriginalImagePath)
            aHashOriginal = aHash(aOriginalImage, hash_size=lHashSize)
            if oCache:
                oCache.set(sOriginalImageCacheKey, aHashOriginal)

        if aHashComparative is None:
            aComparativeImage = load_image(sComparativeImagePath)
            aHashComparative = aHash(aComparativeImage, hash_size=lHashSize)
            if oCache:
                oCache.set(sComparativeImageCacheKey, aHashOriginal)

        # calculate deviation
        dDeviation = hamming_distance(aHashComparative, aHashOriginal)

        # make decision
        bDecision = False
        if(dDeviation <= lThreshold):
            # images are considered to be the same
            bDecision = True

        # push decision to array of decisions
        aDecisions.append(bDecision)

    # return decision and dictionary of metadata
    return aDecisions, dicMetadata


#------------------------------------------------------------------------------#
"""Wrapper for dHash"""


def test_dHash(aOriginalImages, aComparativeImages, lThreshold=0.2, lHashSize=16, oCache=None):

    # create dictionary of metadata
    dicMetadata = {"algorithm": "dHash",
                   "hash_size": lHashSize, "threshold": lThreshold}

    # compare every image
    aDecisions = []
    for i, sOriginalImagePath in enumerate(aOriginalImages):
        sComparativeImagePath = aComparativeImages[i]

        if oCache:
            # create unique cache key for original and comparative key
            aCacheKeyBase = ["dHash", lHashSize]
            sOriginalImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sOriginalImagePath)
            sComparativeImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sComparativeImagePath)

            # check for existence of keys in cache
            aHashOriginal = oCache.get(sOriginalImageCacheKey)
            aHashComparative = oCache.get(sComparativeImageCacheKey)

        # get images from path and calculate hash if not in hash already
        # add to cache if calculated the first time and cache is active
        if aHashOriginal is None:
            aOriginalImage = load_image(sOriginalImagePath)
            aHashOriginal = aHash(aOriginalImage, hash_size=lHashSize)
            if oCache:
                oCache.set(sOriginalImageCacheKey, aHashOriginal)

        if aHashComparative is None:
            aComparativeImage = load_image(sComparativeImagePath)
            aHashComparative = aHash(aComparativeImage, hash_size=lHashSize)
            if oCache:
                oCache.set(sComparativeImageCacheKey, aHashOriginal)

        # calculate deviation
        dDeviation = hamming_distance(aHashComparative, aHashOriginal)

        # make decision
        bDecision = False
        if(dDeviation <= lThreshold):
            # images are considered to be the same
            bDecision = True

        # push decision to array of decisions
        aDecisions.append(bDecision)

    # return decision and dictionary of metadata
    return aDecisions, dicMetadata


#------------------------------------------------------------------------------#
"""Wrapper for pHash"""


def test_pHash(aOriginalImages, aComparativeImages, lThreshold=0.2, dSize=8, dFactor=4, oCache=None):

    # create dictionary of metadata
    dicMetadata = {"algorithm": "dHash",
                   "hash_size": dSize*dFactor, "threshold": lThreshold}

    # compare every image
    aDecisions = []
    for i, sOriginalImagePath in enumerate(aOriginalImages):
        sComparativeImagePath = aComparativeImages[i]

        if oCache:
            # create unique cache key for original and comparative key
            aCacheKeyBase = ["pHash", dSize, dFactor]
            sOriginalImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sOriginalImagePath)
            sComparativeImageCacheKey = oCache.calc_unique_key(
                *aCacheKeyBase, sComparativeImagePath)

            # check for existence of keys in cache
            aHashOriginal = oCache.get(sOriginalImageCacheKey)
            aHashComparative = oCache.get(sComparativeImageCacheKey)

        # get images from path and calculate hash if not in hash already
        # add to cache if calculated the first time and cache is active
        if aHashOriginal is None:
            aOriginalImage = load_image(sOriginalImagePath)
            aHashOriginal = pHash(aOriginalImage, dSize=dSize, dFactor=dFactor)
            if oCache:
                oCache.set(sOriginalImageCacheKey, aHashOriginal)

        if aHashComparative is None:
            aComparativeImage = load_image(sComparativeImagePath)
            aHashComparative = pHash(
                aComparativeImage,  dSize=dSize, dFactor=dFactor)
            if oCache:
                oCache.set(sComparativeImageCacheKey, aHashOriginal)

        # calculate deviation
        dDeviation = hamming_distance(aHashComparative, aHashOriginal)

        # make decision
        bDecision = False
        if(dDeviation <= lThreshold):
            # images are considered to be the same
            bDecision = True

        # push decision to array of decisions
        aDecisions.append(bDecision)

    # return decision and dictionary of metadata
    return aDecisions, dicMetadata
