#!/usr/bin/env python3
from twizzle import TestRunner, Cache
import example_wrapper as wrapper
import numpy as np

# global config
NR_OF_THREADS = 10


if __name__ == "__main__":
    sDBPath = "test.db"

    oRunner = TestRunner(sDBPath, lNrOfThreads=NR_OF_THREADS)
    # create cache
    # here we use a persistent cache because we have to
    oTwizzlePersistentCache = Cache(
        bPersistent=True, sPathToPersistenceDB="twizzle_cache.db")

    # iterate over thresholds
    for lThreshold in np.arange(0.1, 0.3, 0.1):
        # iterate over hash sizes
        for lHashSize in [8, 16, 32]:
            # add test to testrunner
            oRunner.run_test_async("image_hashing_challenge_print_scan_1", wrapper.test_aHash, {
                                   "lThreshold": lThreshold, "lHashSize": lHashSize, "oCache": oTwizzlePersistentCache})
            oRunner.run_test_async("image_hashing_challenge_print_scan_1", wrapper.test_dHash, {
                                   "lThreshold": lThreshold, "lHashSize": lHashSize, "oCache": oTwizzlePersistentCache})
            # # NOTE: for better understanding, this is what
            # # we do here if we would not use threads
            # pm.run_test("printscan_printer1", test_dhash, {"lThreshold":
            # lThreshold, "lHashSize": lHashSize})

    oRunner.wait_till_tests_finished()
