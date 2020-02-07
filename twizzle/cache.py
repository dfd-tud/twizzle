from threading import Lock
from sqlitedict import SqliteDict

CACHE_KEY = "TWIZZLE_CACHE"


class Cache(object):
    """ Cache -- Key-Value Store for Twizzle to reduce unnecessary recomputations
    """

    def __init__(self, bPersistent=False, sPathToPersistenceDB="twizzle_cache.db"):
        """Constructor of the Twizzle Cache

        Note:
            You can decide whether the Chache should be persistent between multiple executions or
            just a runtime cache for one execution of a set of tests
        Args:
            bPersistent (bool): Flag whether the chache should be persistent or not (Note: persistent cache
            is much slower because it has to write the data to the harddisk)

            sPathToPersistenceDB (str): Path to the Cache DB where the Cache should write its data to
        """
        self._cache = {}
        self._lock = Lock()
        self._persistent = bPersistent
        self._first_get = True

        if bPersistent:
            if not sPathToPersistenceDB:
                raise Exception(
                    "On persistent mode a path to the persistence database has to be defined")
            self._db = SqliteDict(sPathToPersistenceDB)

    def set(self, sKey, oValue):
        """set cache element by key"""
        # debug
        print("ADDING CACHELINE: %s" % (sKey))
        self._lock.acquire()
        self._cache[sKey] = oValue
        if self._persistent:
            self._db[CACHE_KEY] = self._cache
            self._db.commit()
        self._lock.release()

    def get(self, sKey):
        """get cache element by key"""

        if self._persistent:
            self._lock.acquire()
            if self._first_get:
                self._first_get = False
                self._cache = self._db.get(CACHE_KEY, {})
            self._lock.release()
        return self._cache.get(sKey, None)

    def calc_unique_key(self, *params):
        """create a unique key based on parameters given by converting them
        to string and concatenating them"""
        return "".join([str(elem) for elem in params])
