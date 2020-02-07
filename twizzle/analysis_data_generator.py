
import pandas as pd
from twizzle import Twizzle


class AnalysisDataGenerator(object):
    """Generator for analysis data in pandas format
    """

    def __init__(self, sDBPath):
        """Constructor of the AnalysisDataGenerator class

        Note:
            Please define the `DB_PATH` in the config.py or pass the path of the SQLite
            as parameter
        Args:
            sDBPath (str): Path to the SQLite database.
        """
        if sDBPath is None:
            raise Exception("Path to SQL-Database has to be defined")
        tw = Twizzle(sDBPath)
        dfChallenges = pd.DataFrame(tw.get_challenges())
        if dfChallenges.empty:
            raise Exception("currently there are no challenges defined yet")
        dfTests = pd.DataFrame(tw.get_tests())
        if dfTests.empty:
            raise Exception("currently no test have been run yet")
        dfChallenges = dfChallenges.drop(
            labels=["originalObjects", "comparativeObjects", "targetDecisions"], axis=1)
        dfTests = pd.merge(dfTests, dfChallenges, how="inner",
                           left_on="challenge", right_on="challenge")
        self.dataframe = dfTests

    def get_pandas_dataframe(self):
        """ get concatenated analysis data as pandas dataframe
        Returns:
            Pandas Dataframe concatenating all challenges with all tests and parameters
        """
        return self.dataframe

    def save_pandas_dataframe_to_file(self, sPathToFile):
        """ save concatenated analysis data as pandas dataframe to CSV file
        """
        if not sPathToFile:
            raise Exception("path to file not specified")
        self.dataframe.to_csv(sPathToFile)
