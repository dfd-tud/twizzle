#!/usr/bin/env python3

from sqlitedict import SqliteDict
import numpy as np

DB_CHALLENGES_KEY = 'challenges'
DB_TESTS_KEY = 'tests'


class Twizzle(object):
    """Twizzle multi purpose benchmarking system -- base class
    """

    def __init__(self, sDBPath):
        """Constructor of the Twizzle class

        Note:
            Please pass the path of the SQLite
            as parameter
        Args:
            sDBPath (str): Path to the SQLite database.
        """
        if sDBPath is None:
            raise Exception("Path to SQL-Database has to be defined")
        self._db = SqliteDict(sDBPath)

    def add_challenge(self, sName, aOriginalObjects, aComparativeObjects, aTargetDecisions, dicMetadata={}):
        """Adds a challenge under the given name to the database

        Note:
            The three lists describe a table of the following format:

            | Original object | Comparative object | target decision |
            |----------------|-------------------|-----------------|
            | Img1.png       | Img1_scaled.png   | True            |
            | Img2.png       | Img2_brighter.png | True            |
            | Img2.png       | Img9.png          | False           |


        Args:
            sName (str): the name of the challenge.
            aOriginalObjects (:obj:`list` of :obj:`str`): List of paths of the original objects
            aComparativeObjects (:obj:`list` of :obj:`str`): List of paths of the objects that should be compared to
                                                            the original objects at the same position in the list
            aTargetDecisions (:obj:`list` of :obj:`bool`): List of boolean defining whether the objects linked in aOriginalObjects
                                                            and aComparativeObjects beeing at the same position in the list are
                                                            the same (True) or not (False)
            dicMetadata (:obj:): an object defining metadata for the challenge like what printer was used or what kind of attack
                                using which parameters was performed

        Returns:
            None
        """

        # catch wrong parameters
        if (not sName) or (aOriginalObjects is None) or (aComparativeObjects is None) or (aTargetDecisions is None):
            raise Exception("Parameters can not be None.")
        if not(len(aOriginalObjects) == len(aComparativeObjects) == len(aTargetDecisions)):
            raise Exception(
                "Objects sets and target decisions have to have the same amount of entries.")
        if not (all(isinstance(x, str) for x in aOriginalObjects) and all(isinstance(x, str) for x in aComparativeObjects)):
            raise Exception(
                "All objects have to be defined as path given as string.")
        if (not all(isinstance(x, bool) for x in aTargetDecisions)) and not isinstance(aTargetDecisions, np.ndarray) and not (aTargetDecisions.dtype == np.dtype("bool")):
            raise Exception("The target decisions have to be boolean only.")

        # get current challenges from database
        aChallenges = self._db.get(DB_CHALLENGES_KEY, [])

        # test whether name was used before
        aChallengesSameName = [
            ch for ch in aChallenges if ch["challenge"] == sName]
        if len(aChallengesSameName) != 0:
            raise Exception(
                "Challenge name %s is already in use. Define an other one. Aborting." % sName)

        # append new challenge
        dicChallenge = {"challenge": sName, "originalObjects": aOriginalObjects,
                        "comparativeObjects": aComparativeObjects, "targetDecisions": aTargetDecisions}
        # adding additional information if given
        if dicMetadata:
            dicChallenge = {**dicMetadata, **dicChallenge}
        aChallenges.append(dicChallenge)
        self._db[DB_CHALLENGES_KEY] = aChallenges
        self._db.commit()

    def del_challenge(self, sName):
        """ deletes an existing challenge by its name

        Args:
            sName (str): the name of the challenge to be deleted

        Returns:
            None
        """

        # get current challenges from database
        aChallenges = self._db.get(DB_CHALLENGES_KEY, [])
        aMatches = [ch for ch in aChallenges if ch["challenge"] == sName]
        if len(aMatches) == 0:
            raise Exception("No challenge named %s found." % sName)

        # remove element
        aChallenges.remove(aMatches[0])

        # save new db
        self._db[DB_CHALLENGES_KEY] = aChallenges
        self._db.commit()

    def get_challenges(self):
        """ getting a list of all defined challenges

        Returns:
            :obj:`list` of :obj:: `obj`:  List of all defined challenges
        """
        return self._db.get(DB_CHALLENGES_KEY, [])

    def get_challenge(self, sChallengeName):
        """ getting a single challenge object

        Args:
            sChallengeName (str): the name of the challenge to get

          Returns:
            :obj:: `obj`:  Object defining the challenge having the name sChallengeName
        """
        aChallenges = self._db.get(DB_CHALLENGES_KEY, [])
        aMatches = [ch for ch in aChallenges if ch["challenge"]
                    == sChallengeName]
        if len(aMatches) == 0:
            raise Exception("No challenge with name %s found." %
                            sChallengeName)
        return aMatches[0]

    def clear_challenges(self):
        """ clears all challenge entries from the database """
        self._db[DB_CHALLENGES_KEY] = []
        self._db.commit()

    def run_test(self, sChallengeName, fnCallback, dicCallbackParameters={}, autosave_to_db=False):
        """ run single challenge as test using given callback function and optional params

        Note:
            fnCallback has to fullfill following specifications

            Parameters:
            fnCallback(aOriginalObjects, aComparativeObjects, **dicCallbackParameters)
            - aOriginalObjects: list of strings describing paths to original objects
            - aComparativeObjects: list of strings describing paths to comparative objects
            ... arbitrary number of further parameters

            Returns:
            aDecisions, dicAdditionalInformation = fnCallback(...)
            - aDecisions: list of boolean decisions describing wether the algorithm has decided that the original object
                          and the comparative objects are the same (True) or not (False)
            - dicAdditionalInformation: the algorithm can supply additional information that can be used in the evaluation
                                        later on to compare different settings


        Args:
            sChallengeName (str): the challenge that should be executed
            fnCallback (function): Pointer to wrapper-function that tests a challenge on a specific algorithm
                                    and makes decisions whether the objects are the same or not depending on its decision algorithm
            dicCallbackParameters (:obj:): Dictionary defining parameters for the function in fnCallback

        Returns:
            dicTest: dictionary of test results that can be saved to db
        """
        if not(sChallengeName) or not(fnCallback):
            raise Exception("Parameters are not allowed to be None.")

        dicChallenge = self.get_challenge(sChallengeName)
        sChallengeName = dicChallenge["challenge"]
        aOriginalObjects = dicChallenge["originalObjects"]
        aComparativeObjects = dicChallenge["comparativeObjects"]
        aTargetDecisions = dicChallenge["targetDecisions"]

        # run challenge
        aDecisions, dicAdditionalInformation = fnCallback(
            aOriginalObjects, aComparativeObjects, **dicCallbackParameters)

        # check if site of decisions is right
        if len(aDecisions) != len(aTargetDecisions):
            raise Exception(
                "Array of Decisions is not the same size as given set of objects. Aborting.")

        # calculate rates
        lTP = np.sum(np.logical_and(
            aDecisions, aTargetDecisions))
        lTN = np.sum(np.logical_and(
            np.logical_not(aDecisions), np.logical_not(aTargetDecisions)))
        lFP = np.sum(np.logical_and(
            aDecisions, np.logical_not(aTargetDecisions)))
        lFN = np.sum(np.logical_and(
            np.logical_not(aDecisions), aTargetDecisions))

        #True positive Rate / Recall -- Robustness in PIH
        dTPR = lTP / (lTP + lFN) if ((lTP+lFN)>0) else 0.
        # True negative Rate -- Sensitivity
        dTNR = lTN / (lTN + lFP) if ((lTN+lFP)>0) else 0.
        # False positive Rate / FAR
        dFPR = 1 - dTNR
        # False negative Rate / FRR
        dFNR = 1 - dTPR

        dAccuracy = (lTP+lTN)/(lTP+lTN+lFP+lFN)
        dPrecision = lTP/(lTP+lFP) if ((lTP+lFP) > 0.) else 0.
        dF1score = 2*((dPrecision*dTPR)/(dPrecision+dTPR)) if ((dPrecision+dTPR)>0) else 0.


        # fill test object
        dicTest = dicAdditionalInformation
        dicTest["challenge"] = sChallengeName
        #dicTest["TP"] = lTP
        #dicTest["TN"] = lTN
        #dicTest["FP"] = lFP
        #dicTest["FN"] = lFN
        dicTest["TPR"] = dTPR #Recall
        dicTest["TNR"] = dTNR
        dicTest["FPR"] = dFPR # FAR
        dicTest["FNR"] = dFNR #FRR

        dicTest["Accuracy"] = dAccuracy
        dicTest["Precision"] = dPrecision
        dicTest["F1_score"] = dF1score


        # save test in db
        if autosave_to_db:
            self.__save_test(dicTest)

        return dicTest

    def __save_test(self, dicTest):
        """ saves a test object to the database"""
        if not dicTest:
            raise Exception("Test object must not be None.")

        aTests = self._db.get(DB_TESTS_KEY, [])
        aTests.append(dicTest)
        self._db[DB_TESTS_KEY] = aTests
        self._db.commit()

    def save_test_threadsafe(self, dicTest, lock):
        """ saves a test object to the database threadsafe"""
        lock.acquire()
        self.__save_test(dicTest)
        lock.release()

    def get_tests(self):
        """getting all tests

        Returns:
            :obj:`list` of :obj:: `obj`:  List of all tests executed
        """
        return self._db.get(DB_TESTS_KEY, [])

    def clear_tests(self):
        """ delete all tests from the database """
        self._db[DB_TESTS_KEY] = []
        self._db.commit()
