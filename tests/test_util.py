import unittest
import pandas as pd
import sys, os
 
sys.path.append(os.path.abspath(os.path.join('../..')))
sys.path.append(os.path.abspath(os.path.join('../src/pypoint/scripts')))

from util import Util

class TestUtils(unittest.TestCase):
    """
    A class for unit-testing function in the fix_clean_tweets_dataframe.py file
    Args:
        -----
    unittest.TestCase this allows the new class to inherit
    from the unittest module
    """

    def setUp(self) -> pd.DataFrame:
        self.util = Util()
        # tweet_df = self.df.get_tweet_df()         


    def test_convert_epsg(self):
        pass
        p3857 = [-10423171.940, 5164494.710]
        p4326 = [-93.63294662707723, 42.02346282729469]
        
        value = self.util.convert_EPSG(3857, 4326, p3857[0], p3857[1])
        self.assertEqual(value, p4326)

if __name__ == '__main__':
    unittest.main()