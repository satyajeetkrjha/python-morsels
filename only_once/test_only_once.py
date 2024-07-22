import unittest
from only_once import only_once  # assuming your only_once function is defined in only_once.py


class OnlyOnceTests(unittest.TestCase):

    """Tests for only_once."""

    def test_function_call_once(self):
        def func(x, y):
            return x + y

        func_once = only_once(func)
        self.assertEqual(func_once(1, 2), 3)

    def test_function_call_twice(self):
        def func(x, y):
            return x + y

        func_once = only_once(func)
        func_once(1, 2)
        with self.assertRaises(ValueError):
            func_once(1, 2)

    def test_function_call_with_different_args(self):
        def func(x, y):
            return x + y

        func_once = only_once(func)

        self.assertEqual(func_once(1, 2), 3)
        with self.assertRaises(ValueError):
            func_once(3, 4)

    def test_function_call_with_keyword_args(self):
        def func(x, y):
            return x + y

        func_once = only_once(func)
        self.assertEqual(func_once(x=1, y=2), 3)
        with self.assertRaises(ValueError):
            func_once(x=3, y=4)

    def test_decorating_functions_with_no_args(self):
        def func():
            return "hello"

        func_once = only_once(func)
        self.assertEqual(func_once(), "hello")
        with self.assertRaises(ValueError):
            func_once()


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2)
