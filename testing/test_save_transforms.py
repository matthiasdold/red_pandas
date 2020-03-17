import unittest
import red_pandas as rpd
import numpy as np


class TestSavetransforms(unittest.TestCase):


    # Understand how to initialize with fixture in a nicer way
    def test_save_groupby_general(self):
        self.df = rpd.RedPandasFrame({'A': ['a', 'b', 'a', np.nan], 'B': [1, 2, 3, 4]})
        result = self.df.save_groupby(['A'], as_index=False)['B'].sum() == rpd.RedPandasFrame({'A': ['a', 'b', np.nan],
                                             'B': [4, 2, 4]
                                             }).fillna('nan')
        self.assertTrue(result.all().all())

    def test_save_groupby_string_input(self):
        self.df = rpd.RedPandasFrame({'A': ['a', 'b', 'a', np.nan], 'B': [1, 2, 3, 4]})
        result = self.df.save_groupby(['A'])['B'].sum() == self.df.save_groupby('A')['B'].sum()
        self.assertTrue(result.all().all())


if __name__ == '__main__':
    unittest.main()
