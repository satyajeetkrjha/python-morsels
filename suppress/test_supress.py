from types import TracebackType
import unittest

from suppress import suppress


class SuppressTests(unittest.TestCase):

    """Tests for suppress."""

    def test_works_when_no_exception_raised(self):
        with suppress(Exception):
            x = 4
        self.assertEqual(x, 4)

    def test_suppress_specific_exception(self):
        with suppress(ValueError):
            x = 1
            int('hello')
            x = 2
        self.assertEqual(x, 1)
        with suppress(TypeError):
            x = 3
            int(None)
            x = 4
        self.assertEqual(x, 3)

    def test_keyerror_and_index_error(self):
        with suppress(KeyError):
            my_dict = {'key': 'value'}
            my_dict[4]
        self.assertEqual(my_dict, {'key': 'value'})
        with suppress(IndexError):
            my_list = ['item']
            my_list[1]
            self.assertEqual(my_list, ['item'])

    def test_suppresses_parent_exceptions(self):
        with suppress(LookupError):
            my_dict = {'key': 'value'}
            my_dict[4]
        self.assertEqual(my_dict, {'key': 'value'})
        with suppress(LookupError):
            my_list = ['item']
            my_list[1]
            self.assertEqual(my_list, ['item'])

    def test_does_not_suppress_other_exceptions(self):
        with self.assertRaises(KeyError):
            with suppress(IndexError):
                my_dict = {'key': 'value'}
                my_dict[4]
            self.assertEqual(my_dict, {'key': 'value'})
        with self.assertRaises(IndexError):
            with suppress(KeyError):
                my_list = ['item']
                my_list[1]
                self.assertEqual(my_list, ['item'])

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_catches_any_number_of_exceptions(self):
        with suppress(ValueError, TypeError):
            int('hello')
        with suppress(IndexError, TypeError):
            int(None)
        with self.assertRaises(KeyError):
            with suppress(IndexError, TypeError):
                {0: 1}[1]
        with suppress(ValueError, SystemError, IndexError, TypeError):
            ['item'][1]

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_allows_exception_to_be_viewed(self):
        with suppress(LookupError) as suppressed:
            my_dict = {'key': 'value'}
            my_dict[4]
        self.assertEqual(type(suppressed.exception), KeyError)
        self.assertEqual(type(suppressed.traceback), TracebackType)
        with suppress(LookupError) as suppressed:
            my_dict = {'key': 'value'}
            my_dict['key']
        self.assertIs(suppressed.exception, None)
        self.assertIs(suppressed.traceback, None)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_works_as_a_decorator(self):
        @suppress(TypeError)
        def len_or_none(thing):
            return len(thing)
        self.assertEqual(len_or_none(['a', 'b', 'c']), 3)
        self.assertEqual(len_or_none(3.5), None)


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
