from twizzle import Twizzle
from multiprocessing.pool import ThreadPool
from threading import Lock


class TestRunner(object):
    """ TestRunner - creates a multi threaded environment for running tests
    """

    def __init__(self, sDBPath, lNrOfThreads=2):
        """Constructor of a TestRunner class

        Note:
            Please define the `DB_PATH` in the config.py or pass the path of the SQLite 
            as parameter
        Args:
            sDBPath (str): Path to the SQLite database.
            lNrOfThreads (int): number of threads to use for the tests
        """
        if sDBPath is None:
            raise Exception("Path to SQL-Database has to be defined")
        if lNrOfThreads <= 0:
            raise Exception("lNrOfThreads has to be grater then 0")
        self.tw = Twizzle(sDBPath)
        self.oPool = ThreadPool(processes=lNrOfThreads)
        self.aTaskPoolThreads = []
        self.lock = Lock()

    def run_test_async(self, sChallengeName, fnCallback, dicCallbackParameters={}):
        """add test run to threadpool

        Args:
            sChallengeName (str): name of the challenge that should be tested
            fnCallback (function): test wrapper function that should be called
            dicCallbackParameters (:obj:): Dictionary of parameters for  fnCallback

        Returns:
            None
        """
        pThread = self.oPool.apply_async(
            self.tw.run_test, (sChallengeName, fnCallback, dicCallbackParameters))
        self.aTaskPoolThreads.append(pThread)

    def wait_till_tests_finished(self):
        """block execution till all threads are done"""
        # catch threads ready
        for pThread in self.aTaskPoolThreads:
            dicTest = pThread.get()
            self.tw.save_test_threadsafe(dicTest, self.lock)

    def get_tests(self):
        """get all tests defined"""
        return self.tw.get_tests()
