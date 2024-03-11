import unittest

from count_calls import count_calls


class CountCallsTests(unittest.TestCase):

    """Tests for count_calls."""

    def test_call_count_starts_at_zero(self):
        counter = count_calls()
        self.assertEqual(counter.calls, 0)

    def test_call_count_increments(self):
        counter = count_calls()
        self.assertEqual(counter.calls, 0)
        counter()
        self.assertEqual(counter.calls, 1)
        counter()
        self.assertEqual(counter.calls, 2)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_accepts_and_calls_a_function(self):
        # Function value is returned
        def one(): return 1
        decorated = count_calls(one)
        self.assertEqual(decorated(), 1)
        self.assertEqual(decorated.calls, 1)

        # Function is called each time
        recordings = []
        def my_func():
            recordings.append('call')
            return recordings
        decorated = count_calls(my_func)
        self.assertEqual(recordings, [])
        self.assertEqual(decorated.calls, 0)
        self.assertEqual(decorated(), ['call'])
        self.assertEqual(decorated.calls, 1)
        self.assertEqual(decorated(), ['call', 'call'])
        self.assertEqual(decorated.calls, 2)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_accepts_arguments(self):
        # Function accepts positional arguments
        @count_calls
        def add(x, y):
            return x + y
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(1, 3), 4)

        # Function accepts keyword arguments
        recordings = []
        @count_calls
        def my_func(*args, **kwargs):
            recordings.append((args, kwargs))
            return recordings
        self.assertEqual(my_func(), [((), {})])
        self.assertEqual(my_func(1, 2, a=3), [((), {}), ((1, 2), {'a': 3})])

        # Exceptions are still counted as calls
        @count_calls
        def my_func():
            raise AssertionError("Function called too soon")
        self.assertEqual(my_func.calls, 0)
        with self.assertRaises(AssertionError):
            my_func()
        self.assertEqual(my_func.calls, 1)
        self.assertEqual(my_func.calls, 1)
        with self.assertRaises(AssertionError):
            my_func()
        self.assertEqual(my_func.calls, 2)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_docstring_and_name_preserved(self):
        import pydoc
        decorated = count_calls(example)
        self.assertIn('function example', str(decorated))
        documentation = pydoc.render_doc(decorated)
        self.assertIn('function example', documentation)
        self.assertIn('Example function.', documentation)
        self.assertIn('(a, b=True)', documentation)


def example(a, b=True):
    """Example function."""
    print('hello world')


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
