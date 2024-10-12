from contextlib import (
    contextmanager,
    redirect_stdout,
    redirect_stderr,
)
from io import StringIO
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from time import perf_counter
import unittest
import warnings


class FindDuplicatesTests(unittest.TestCase):

    """Tests for find_duplicates."""

    @contextmanager
    def make_files(self, files, same_dir=False):
        warnings.simplefilter("ignore", ResourceWarning)
        if same_dir:
            tmp_dir = None
            directory = os.getcwd()
        else:
            tmp_dir = TemporaryDirectory()
            directory = tmp_dir.name
        directory = Path(directory)
        cwd = os.getcwd()
        os.chdir(directory)
        try:
            filenames = []
            for name, contents in files:
                path = Path(name)
                path.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(contents, str):
                    path.write_text(contents)
                else:
                    path.write_bytes(contents)
                filenames.append(str(path))
            yield filenames
        finally:
            os.chdir(cwd)
            if tmp_dir:
                tmp_dir.cleanup()

    def assertNoDuplicates(self, arguments):
        self.assertEqual(
            run_program('dups.py', list(arguments)),
            "No duplicate files found\n",
        )

    def assertDuplicates(self, arguments, groups):
        output = run_program('dups.py', list(arguments))
        for n in range(1, len(groups)+1):
            self.assertIn(f"Duplicate group {n}", output)
        self.assertNotIn("Duplicate group 0", output)
        self.assertNotIn(f"Duplicate group {n+1}", output)
        for group in groups:
            self.assertIn("\n".join(sorted(group)), output)

    def test_no_duplicates(self):
        with self.make_files([
                ("a.txt", "file1"),
                ("b.txt", "file2"),
                ("c.txt", "file3"),
        ]) as (target, *others):
            self.assertNoDuplicates([target, *others])

    def test_one_duplicate(self):
        with self.make_files([
                ("a.txt", "file1"),
                ("b.txt", "file2"),
                ("c.txt", "file1"),
        ]) as (target, *others):
            self.assertDuplicates(
                [target, *others],
                [
                    [target, others[-1]],
                ],
            )

    def test_two_duplicates(self):
        with self.make_files([
                ("a.txt", "file1"),
                ("b.txt", "file2"),
                ("c.txt", "file1"),
                ("d.txt", "file3"),
                ("e.txt", "file1"),
        ]) as filenames:
            self.assertDuplicates(
                [filenames[0], *filenames[1:]],
                [
                    [filenames[0], filenames[2], filenames[4]],
                ],
            )

    def test_non_text_files(self):
        with self.make_files([
                ("a.txt", "file1"),
                ("b.txt", bytes(range(256))),
                ("c.txt", "file1"),
                ("d.txt", "file3"),
                ("e.txt", bytes(range(256))),
                ("f.txt", "a" * 256),
        ]) as filenames:
            self.assertDuplicates(
                filenames,
                [
                    [filenames[0], filenames[2]],
                    [filenames[1], filenames[4]],
                ],
            )

    def test_three_groups_of_duplicates(self):
        with self.make_files([
                ("a.txt", "Hello there"),
                ("b.txt", "Hi"),
                ("c.txt", "Hello hello"),
                ("d.txt", "Hey"),
                ("e.txt", "Hello hello"),
                ("f.txt", "Hi"),
                ("g.txt", "Hello"),
                ("h.txt", "Hi"),
                ("i.txt", "Hey"),
        ]) as filenames:
            self.assertDuplicates(
                filenames,
                [
                    [filenames[1], filenames[5], filenames[7]],
                    [filenames[2], filenames[4]],
                    [filenames[3], filenames[8]],
                ],
            )

    def test_compares_efficiently(self):
        contents = [
            bin(i)
            for i in range(992)
        ] + ["0b0", "0b1"]
        filenames = [
            (f"file{n}.txt", c)
            for n, c in enumerate(contents)
        ]
        with self.make_files(filenames[:75]) as files:
            self.assertNoDuplicates(files)
            with Timer() as t5:
                self.assertNoDuplicates(files[:5])
            with Timer() as t75:
                self.assertNoDuplicates(files[:75])
            self.assertLess(t75.elapsed, t5.elapsed * 150)
            with self.make_files(
                filenames[75:250],
                same_dir=True,
            ) as more_files:
                files += more_files
                with Timer() as t250:
                    self.assertNoDuplicates(files[:250])
                self.assertLess(t250.elapsed, t75.elapsed * 65)
                self.assertLess(t250.elapsed, t5.elapsed * 500)
                with self.make_files(
                    filenames[250:],
                    same_dir=True
                ) as more_files:
                    files += more_files
                    self.assertDuplicates(files, [
                        [files[0], files[-2]],
                        [files[1], files[-1]],
                    ])
                    with Timer() as t1000:
                        self.assertDuplicates(
                            files[:1000],
                            [
                                [files[0], files[-2]],
                                [files[1], files[-1]],
                            ],
                        )
                    self.assertLess(t1000.elapsed, t75.elapsed * 150)
                    self.assertLess(t1000.elapsed, t5.elapsed * 1300)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_search_directories_recursively(self):
        with self.make_files([
                ("X/a.txt", "Hello there"),
                ("X/b.txt", "Hi"),
                ("c.txt", "Hello hello"),
                ("Y/d.txt", "Hey"),
                ("e.txt", "Hello hello"),
                ("Y/b.txt", "Hi"),
                ("f.txt", "Hello"),
                ("Z/g.txt", "Hi"),
                ("X/h.txt", "Hey"),
        ]) as filenames:
            Path("X/W").mkdir()
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z"],
                [
                    [filenames[1], filenames[5], filenames[7]],
                    [filenames[3], filenames[8]],
                ],
            )
            self.assertDuplicates(
                ["."],
                [
                    [filenames[1], filenames[5], filenames[7]],
                    [filenames[2], filenames[4]],
                    [filenames[3], filenames[8]],
                ],
            )

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_min_size_argument(self):
        with self.make_files([
                ("X/a.txt", "Hello there"),
                ("X/b.txt", "Hi"),
                ("c.txt", "Hello hello"),
                ("Y/d.txt", "Hey"),
                ("e.txt", "Hello hello"),
                ("Y/b.txt", "Hi"),
                ("f.txt", "Hello"),
                ("Z/g.txt", "Hi"),
                ("X/h.txt", "Hey"),
        ]) as filenames:
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=2"],
                [
                    [filenames[1], filenames[5], filenames[7]],
                    [filenames[2], filenames[4]],
                    [filenames[3], filenames[8]],
                ],
            )
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=3"],
                [
                    [filenames[2], filenames[4]],
                    [filenames[3], filenames[8]],
                ],
            )
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=4"],
                [
                    [filenames[2], filenames[4]],
                ],
            )
            self.assertNoDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=15"],
            )

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_ignore_argument(self):
        with self.make_files([
                ("X/a.txt", "Hello there"),
                ("X/b.txt", "Hi"),
                ("c.txt", "Hello hello"),
                ("Y/d.txt", "Hey"),
                ("e.txt", "Hello hello"),
                ("Y/b.txt", "Hi"),
                ("f.txt", "Hello"),
                ("Z/g.txt", "Hi"),
                ("X/h.txt", "Hey"),
        ]) as filenames:
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--ignore=b.txt"],
                [
                    [filenames[2], filenames[4]],
                    [filenames[3], filenames[8]],
                ],
            )
            self.assertDuplicates(
                [".", "--ignore=X"],
                [
                    [filenames[5], filenames[7]],
                    [filenames[2], filenames[4]],
                ],
            )
            self.assertDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=4"],
                [
                    [filenames[2], filenames[4]],
                ],
            )
            self.assertNoDuplicates(
                ["X", "c.txt", "Y", "Z", "e.txt", "--min-size=15"],
            )


class Timer:

    """Context manager to time a code block."""

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, *args):
        self.end = perf_counter()
        self.elapsed = self.end - self.start


class DummyException(Exception):
    """No code will ever raise this exception."""


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(path, args=[], raises=DummyException):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            with redirect_stderr(output):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    loader = SourceFileLoader('__main__', path)
                    spec = spec_from_loader(loader.name, loader)
                    module = module_from_spec(spec)
                    sys.modules['__main__'] = module
                    loader.exec_module(module)
                except raises:
                    return output.getvalue()
                except SystemExit as e:
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
                return output.getvalue()
    finally:
        sys.argv = old_args


if __name__ == "__main__":
    unittest.main(verbosity=2)
