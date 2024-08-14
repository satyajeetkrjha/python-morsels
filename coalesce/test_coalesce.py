import unittest


from coalesce import coalesce


class CoalesceTests(unittest.TestCase):

    """Tests for coalesce."""

    def test_coalesce_to_empty_string(self):
        self.assertEqual(coalesce("Trey", ""), "Trey")
        self.assertEqual(coalesce("", ""), "")
        self.assertEqual(coalesce(None, ""), "")
        self.assertEqual(coalesce(4, ""), 4)

    def test_coalasce_to_empty_list(self):
        self.assertEqual(coalesce("Trey", []), "Trey")
        self.assertEqual(coalesce("", []), "")
        self.assertEqual(coalesce(None, []), [])
        self.assertEqual(coalesce([1, 2, 3], []), [1, 2, 3])
        x = []
        self.assertEqual(coalesce(x, []), x)
        self.assertIs(coalesce(x, []), x)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_sentinel_argument(self):
        # None sentinel
        self.assertEqual(coalesce("Trey", "", sentinel=None), "Trey")
        self.assertEqual(coalesce("", [], sentinel=None), "")
        self.assertEqual(coalesce(None, "", sentinel=None), "")
        self.assertEqual(coalesce(None, [], sentinel=None), [])

        # Empty string sentinel
        self.assertEqual(coalesce("Trey", "world", sentinel=""), "Trey")
        self.assertEqual(coalesce("", "world", sentinel=""), "world")
        self.assertEqual(coalesce(None, "world", sentinel=""), None)

        # Both empty string and None sentinel
        self.assertEqual(coalesce("Trey", "world", sentinel=("", None)), "Trey")
        self.assertEqual(coalesce("", "world", sentinel=("", None)), "world")
        self.assertEqual(coalesce(None, "world", sentinel=("", None)), "world")

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_any_number_of_arguments(self):
        self.assertEqual(coalesce("Trey", None, "", sentinel=None), "Trey")
        self.assertEqual(coalesce("", None, "Trey", sentinel=None), "")
        self.assertEqual(coalesce(None, "", "Trey", sentinel=None), "")
        self.assertEqual(coalesce(None, "Trey", "", sentinel=None), "Trey")
        self.assertEqual(coalesce(None, None, None, "", sentinel=None), "")
        with self.assertRaises(ValueError):
            coalesce(None, None, None, None, None, sentinel=None)


# To test bonus 3, comment out the next line
@unittest.expectedFailure
class CoalesceAllTests(unittest.TestCase):

    """Tests for coalesce_all."""

    def test_coalesce_one_argument(self):
        from coalesce import coalesce_all
        @coalesce_all("world")
        def greet(greet="world"):
            return "Hello {}".format(greet)
        self.assertEqual(greet("Trey"), "Hello Trey")
        self.assertEqual(greet("someone"), "Hello someone")
        self.assertEqual(greet(""), "Hello ")
        self.assertEqual(greet(None), "Hello world")
        self.assertEqual(greet(), "Hello world")

    def test_coalesce_one_argument_from_empty_string(self):
        from coalesce import coalesce_all
        @coalesce_all("world", sentinel="")
        def greet(greet="world"):
            return "Hello {}".format(greet)
        self.assertEqual(greet("Trey"), "Hello Trey")
        self.assertEqual(greet("someone"), "Hello someone")
        self.assertEqual(greet(""), "Hello world")
        self.assertEqual(greet(None), "Hello None")
        self.assertEqual(greet(), "Hello world")

    def test_coalesce_one_argument_from_multiple_values(self):
        from coalesce import coalesce_all
        @coalesce_all("world", sentinel=(None, ""))
        def greet(greet="world"):
            return "Hello {}".format(greet)
        self.assertEqual(greet("Trey"), "Hello Trey")
        self.assertEqual(greet("someone"), "Hello someone")
        self.assertEqual(greet(""), "Hello world")
        self.assertEqual(greet(None), "Hello world")
        self.assertEqual(greet(), "Hello world")

    def test_coalesce_multiple_arguments(self):
        from coalesce import coalesce_all
        @coalesce_all(1)
        def multiply(x, y):
            return x * y
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(None, None), 1)
        self.assertEqual(multiply(2, None), 2)
        self.assertEqual(multiply(None, 3), 3)
        with self.assertRaises(TypeError):
            multiply(4)
        with self.assertRaises(TypeError):
            multiply()

    def test_coalesce_keyword_arguments(self):
        from coalesce import coalesce_all
        @coalesce_all(1)
        def multiply(x, y):
            return x * y
        self.assertEqual(multiply(x=2, y=3), 6)
        self.assertEqual(multiply(2, y=3), 6)
        self.assertEqual(multiply(x=None, y=None), 1)
        self.assertEqual(multiply(x=2, y=None), 2)
        self.assertEqual(multiply(2, y=None), 2)
        self.assertEqual(multiply(x=None, y=3), 3)
        self.assertEqual(multiply(None, y=3), 3)
        with self.assertRaises(TypeError):
            multiply(x=4)
        with self.assertRaises(TypeError):
            multiply(y=4)


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
