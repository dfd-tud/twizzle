#!/usr/bin/env python3

import pandas as pd
from twizzle import AnalysisDataGenerator
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # load data in a pandas dataframe
    sDBPath = "test.db"
    dfTests = AnalysisDataGenerator(sDBPath).get_pandas_dataframe()
    ax = plt.gca()
    dfTests.plot(kind='line',x='algorithm', y='TPR/Recall', color='red', ax=ax)
    dfTests.plot(kind='line',x='algorithm', y='Precision', color='blue', ax=ax)
    plt.show()

    # do something with the dataframe
    print(dfTests)
