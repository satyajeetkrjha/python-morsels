from timeit import repeat
import unittest

from uniques import uniques_only


class UniquesOnlyTests(unittest.TestCase):

    """Tests for uniques_only."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_no_duplicates(self):
        self.assertIterableEqual(uniques_only([1, 2, 3]), [1, 2, 3])

    def test_adjacent_duplicates(self):
        self.assertIterableEqual(uniques_only([1, 1, 2, 2, 3]), [1, 2, 3])

    def test_non_adjacent_duplicates(self):
        self.assertIterableEqual(uniques_only([1, 2, 3, 1, 2]), [1, 2, 3])

    def test_lots_of_duplicates(self):
        self.assertIterableEqual(uniques_only([1, 2, 2, 1, 1, 2, 1]), [1, 2])

    def test_order_maintained(self):
        self.assertIterableEqual(
            uniques_only([4, 8, 3, 7, 2, 8, 4, 2, 1, 9, 3, 5]),
            [4, 8, 3, 7, 2, 1, 9, 5],
        )

    def test_accepts_iterator(self):
        nums = (n**2 for n in [1, 2, 3])
        self.assertIterableEqual(uniques_only(nums), [1, 4, 9])

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_returns_iterator(self):
        nums = iter([1, 2, 3])
        output = uniques_only(nums)
        self.assertEqual(iter(output), iter(output))
        self.assertEqual(next(output), 1)
        # The below line tests that the incoming generator isn't exhausted.
        # It may look odd to test the nums input, but this is correct
        # because after 1 item has been consumed from the uniques_only
        # iterator, nums should only have 1 item consumed as well
        try:
            self.assertEqual(next(nums), 2)
        except StopIteration:
            self.fail("The incoming nums iterator was fully consumed!")

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_accepts_nonhashable_types(self):
        output = uniques_only([[1, 2], [3], [1], [3]])
        self.assertIterableEqual(output, [[1, 2], [3], [1]])

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_hashable_types_faster(self):
        hashables = [(n, n+1) for n in range(1000)] + [0]
        unhashables = [[n] for n in range(1000)] + [0]
        variables = {
            "hashables": hashables,
            "unhashables": unhashables,
            "uniques_only": uniques_only,
        }
        hashable_time = min(repeat(
            "list(uniques_only(hashables))",
            number=3,
            repeat=3,
            globals=variables
        ))
        unhashable_time = min(repeat(
            "list(uniques_only(unhashables))",
            number=3,
            repeat=3,
            globals=variables
        ))
        self.assertLess(hashable_time*3, unhashable_time)


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
