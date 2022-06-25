import unittest
import pandas as pd
import sys, os
 
sys.path.append(os.path.abspath(os.path.join('../..')))

from src import pypoint
from extract_dataframe import TweetDfExtractor

class TestUtils(unittest.TestCase):
    """
    A class for unit-testing function in the fix_clean_tweets_dataframe.py file
    Args:
        -----
    unittest.TestCase this allows the new class to inherit
    from the unittest module
    """

    def setUp(self) -> pd.DataFrame:
        self.util = pypoint.scripts.util.Util()
        # tweet_df = self.df.get_tweet_df()         


    def test_find_statuses_count(self):
        self.assertEqual(self.df.find_statuses_count(), [8606, 119, 14551, 6231, 42906])

if __name__ == '__main__':
    unittest.main()