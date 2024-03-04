# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import redirect_stdout
from io import StringIO
import unittest


from count import count_words


class CountWordsTests(unittest.TestCase):

    """Tests for count_words."""

    def test_zreturn_instead_of_print(self):
        with redirect_stdout(StringIO()) as stdout:
            actual = count_words("oh what a day what a lovely day")
        output = stdout.getvalue().strip()
        if actual is None and output:
            self.fail(
                "\n\nUh oh!\n"
                "It looks like you may have printed instead of returning.\n"
                f"None was returned but this was printed:\n{output}"
            )

    def test_simple_sentence(self):
        actual = count_words("oh what a day what a lovely day")
        expected = {'oh': 1, 'what': 2, 'a': 2, 'day': 2, 'lovely': 1}
        self.assertEqual(actual, expected)

    def test_apostrophe(self):
        actual = count_words("don't stop believing")
        expected = {"don't": 1, 'stop': 1, 'believing': 1}
        self.assertEqual(actual, expected)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_capitalization(self):
        actual = count_words("Oh what a day what a lovely day")
        expected = {'oh': 1, 'what': 2, 'a': 2, 'day': 2, 'lovely': 1}
        self.assertEqual(actual, expected)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_symbols(self):
        actual = count_words("Oh what a day, what a lovely day!")
        expected = {'oh': 1, 'what': 2, 'a': 2, 'day': 2, 'lovely': 1}
        self.assertEqual(actual, expected)
        actual = count_words("¿Te gusta Python?")
        expected = {'te': 1, 'gusta': 1, 'python': 1}
        self.assertEqual(actual, expected)


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