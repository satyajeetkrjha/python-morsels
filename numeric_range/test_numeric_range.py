import unittest

from numeric_range import numeric_range


class NumericRangeTests(unittest.TestCase):

    """Tests for numeric_range."""

    def test_ordered_numbers(self):
        self.assertEqual(numeric_range([0, 1, 2, 3, 4]), 4)

    def test_with_out_of_order_numbers(self):
        self.assertEqual(numeric_range([10, 8, 7, 5.0, 3, 6, 2]), 8)

    def test_single_item(self):
        self.assertEqual(numeric_range([10]), 0)

    def test_same_item_multiple_times(self):
        self.assertEqual(numeric_range([8, 8, 8]), 0)
        self.assertEqual(numeric_range([7, 5, 6, 5, 7]), 2)

    def test_negative_numbers(self):
        self.assertEqual(numeric_range([-10, -8, -7, -5, -3]), 7)

    def test_mixed_types(self):
        with self.assertRaises(TypeError):
            numeric_range(['a', 2])

    def test_very_large_numbers(self):
        self.assertEqual(numeric_range([2**1000, -2**1000]), 2**1001)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_returns_zero_for_empty_list(self):
        self.assertEqual(numeric_range([]), 0)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_with_non_lists(self):
        self.assertEqual(numeric_range((89, 17, 70, 9)), 80)
        self.assertEqual(numeric_range({8, 7, 5, 3, 9, 6, 2}), 7)
        self.assertEqual(numeric_range(n**2 for n in range(1, 4)), 8)
        self.assertEqual(numeric_range(n for n in []), 0)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
