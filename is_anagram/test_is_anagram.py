# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import redirect_stdout
from io import StringIO
import unittest

from anagram import is_anagram


class IsAnagramTests(unittest.TestCase):

    """Tests for is_anagram."""

    def test_zreturn_instead_of_print(self):
        with redirect_stdout(StringIO()) as stdout:
            actual = is_anagram("a", "a")
        output = stdout.getvalue().strip()
        if actual is None and output:
            self.fail(
                "\n\nUh oh!\n"
                "It looks like you may have printed instead of returning.\n"
                "See https://pym.dev/print-vs-return/\n"
                f"None was returned but this was printed:\n{output}"
            )

    def test_short_anagram(self):
        self.assertTrue(is_anagram("tea", "eat"))

    def test_different_lengths(self):
        self.assertFalse(is_anagram("tea", "treat"))

    def test_sink_and_skin(self):
        self.assertTrue(is_anagram("sink", "skin"))

    def test_same_letters_different_lengths(self):
        self.assertFalse(is_anagram("sinks", "skin"))
        self.assertFalse(is_anagram("nine", "eine"))

    def test_different_capitalization(self):
        self.assertTrue(is_anagram("Trey", "Yert"))
        self.assertTrue(is_anagram("Listen", "silent"))

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_spaces_ignored(self):
        phrase1 = "William Shakespeare"
        phrase2 = "I am a weakish speller"
        self.assertTrue(is_anagram(phrase1, phrase2))
        self.assertFalse(is_anagram("a b c", "a b d"))

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_punctation_ignored(self):
        phrase1 = "A diet"
        phrase2 = "I'd eat"
        self.assertTrue(is_anagram(phrase1, phrase2))

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_characters_with_accents(self):
        self.assertTrue(is_anagram("Siobhán Donaghy", "Shanghai Nobody"))


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
