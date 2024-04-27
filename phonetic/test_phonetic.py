from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from importlib.util import spec_from_file_location, module_from_spec
import os
from pathlib import Path
import shlex
import sys
from tempfile import NamedTemporaryFile
from textwrap import dedent
import unittest
import warnings


class PhoneticTests(unittest.TestCase):

    """Tests for phonetic.py"""

    def test_all_lowercase(self):
        output = run_program('phonetic.py python')
        self.assertEqual(
            output,
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )

    def test_all_uppercase(self):
        output = run_program('phonetic.py PYTHON')
        self.assertEqual(
            output,
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )

    def test_mixed_case(self):
        output = run_program('phonetic.py Python')
        self.assertEqual(
            output,
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )

    def test_punctuation(self):
        output = run_program('phonetic.py django-rest-framework')
        self.assertEqual(
            output,
            "Delta\nJuliett\nAlfa\nNovember\nGolf\nOscar\n" +
            "Romeo\nEcho\nSierra\nTango\n" +
            "Foxtrot\nRomeo\nAlfa\nMike\nEcho\nWhiskey\nOscar\nRomeo\nKilo\n"
        )

    def test_prompt_when_no_command_line_arguments(self):
        # No arguments and one-word response spells the word
        with patch_stdin('Python!\n'):
            output = run_program('phonetic.py')
        self.assertEqual(
            output,
            "Text to spell out: " +
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )

        # No arguments and empty response prints no words
        with patch_stdin('\n'):
            output = run_program('phonetic.py')
        self.assertEqual(output.rstrip("\n"), "Text to spell out: ")

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_multiple_words(self):
        # Multiple words as separate arguments
        output = run_program('phonetic.py Monty Python')
        self.assertEqual(
            output,
            "Mike\nOscar\nNovember\nTango\nYankee\n" +
            "\n" +
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )
        # Multiple words as one argument
        output = run_program('phonetic.py "Monty Python"')
        self.assertEqual(
            output,
            "Mike\nOscar\nNovember\nTango\nYankee\n" +
            "\n" +
            "Papa\nYankee\nTango\nHotel\nOscar\nNovember\n",
        )

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_alphabet_file(self):
        contents = dedent("""
            a alfa
            b bravo
            c charlie
            d delta
            e echo
            f foxtrot
            g golf
            h hotel
            i india
            j juliett
            k kilo
            l lima
            m mike
            n november
            o oscar
            p papa
            q quebec
            r romeo
            s sierra
            t tango
            u uniform
            v victor
            w whiskey
            x x-ray
            y yankee
            z zulu
            0 zero
            1 wun
            2 too
            3 tree
            4 fower
            5 fife
            6 six
            7 seven
            8 eight
            9 niner
        """).strip()
        with make_file(contents) as letters_file:

            output = run_program(f'phonetic.py -f {letters_file} Hello')
            self.assertEqual(output, "hotel\necho\nlima\nlima\noscar\n")

            output = run_program(f'phonetic.py Python 3 -f {letters_file}')
            self.assertEqual(
                output,
                "papa\nyankee\ntango\nhotel\noscar\nnovember\n" +
                "\n" +
                "tree\n",
            )

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_ignore_accents(self):
        output = run_program('phonetic.py hétérogénéité')
        self.assertEqual(
            output,
            "Hotel\nEcho\nTango\nEcho\nRomeo\nOscar\nGolf\nEcho\nNovember\n" +
            "Echo\nIndia\nTango\nEcho\n"
        )
        output = run_program('phonetic.py ¿un año?')
        self.assertEqual(
            output,
            "Uniform\nNovember\n\nAlfa\nNovember\nOscar\n",
        )


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


class DummyException(Exception):
    """No code will ever raise this exception."""


def run_program(arguments, raises=DummyException, stderr=False):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.

    If stderr is True, separate stdout and stderr streams.
    """
    arguments = arguments.replace("\\", "\\\\")  # shlex posix=True workaround
    [path, *args] = shlex.split(arguments)
    path = str(DIRECTORY / path)
    old_args = sys.argv
    warnings.filterwarnings("ignore", r"unclosed file", ResourceWarning)
    try:
        sys.argv = [path, *args]  # Monkey-patch sys.argv
        with redirect_stdout(StringIO()) as output:
            error = StringIO() if stderr else output
            with redirect_stderr(error):
                try:
                    sys.modules.pop("__main__", None)
                    spec = spec_from_file_location("__main__", path)
                    module = module_from_spec(spec)
                    sys.modules["__main__"] = module
                    spec.loader.exec_module(module)
                # A specific exception should have been raised
                except raises as e:
                    # If sys.exit is called with a string, print it out
                    if isinstance(e, SystemExit):
                        if e.args and not isinstance(e.args[0], int):
                            if len(e.args) == 1:
                                error.write(str(e.args[0]))
                            else:
                                error.write(str(e.args))
                # An unexpected SystemExit exception was raised
                except SystemExit as e:
                    if e.args not in [(0,), (None,)]:
                        raise SystemExit(error.getvalue()) from e
                # No exception was raised
                else:
                    if raises is not DummyException:
                        raise AssertionError("{} not raised".format(raises))
                # Always force delete objects
                finally:
                    sys.modules["__main__"].__dict__.clear()
                    sys.modules.pop("__main__", None)  # Closes any open files

                if stderr:
                    return output.getvalue(), error.getvalue()
                else:
                    return output.getvalue()
    finally:
        sys.argv = old_args  # Undo the monkey patching of sys.argv


@contextmanager
def patch_stdin(text):
    real_stdin = sys.stdin
    sys.stdin = StringIO(text)
    try:
        yield sys.stdin
    except EOFError as e:
        raise AssertionError("Kept prompting for input too long") from e
    finally:
        sys.stdin = real_stdin


@contextmanager
def make_file(contents=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wt', encoding='utf-8', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
