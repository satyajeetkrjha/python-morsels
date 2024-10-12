from contextlib import contextmanager, ExitStack
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from timeit import default_timer
import unittest

from fileutils2 import find_duplicates


class FindDuplicatesTests(unittest.TestCase):

    """Tests for find_duplicates."""

    @contextmanager
    def make_files(self, *file_contents):
        with ExitStack() as stack:
            yield [
                stack.enter_context(make_file(contents))
                for contents in file_contents
            ]

    def assertSameMatches(self, iterable1, iterable2):
        iterable1 = list(iterable1)
        iterable2 = list(iterable2)
        self.assertEqual(
            len(iterable1),
            len(iterable2),
            "{} != {}".format(iterable1, iterable2),
        )
        self.assertEqual(
            {frozenset(i) for i in iterable1},
            {frozenset(i) for i in iterable2},
        )

    def test_no_duplicates(self):
        with self.make_files("file1", "file2", "file3") as (target, *others):
            self.assertSameMatches(find_duplicates([target, *others]), [])

    def test_one_duplicate(self):
        with self.make_files("file1", "file2", "file1") as (target, *others):
            self.assertSameMatches(
                find_duplicates([target, *others]),
                [{target, others[-1]}],
            )

    def test_two_duplicates(self):
        with self.make_files(
            "file1", "file2", "file1", "file3", "file1"
        ) as filenames:
            self.assertSameMatches(
                find_duplicates([filenames[0], *filenames[1:]]),
                [{filenames[0], filenames[2], filenames[4]}],
            )

    def test_non_text_files(self):
        with self.make_files(
            "file1", "file2", "file1", "file3", bytes(range(256)), "a" * 256
        ) as filenames:
            self.assertSameMatches(
                find_duplicates([*filenames]),
                [{filenames[0], filenames[2]}],
            )

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_matches_all_files_against_each_other(self):
        contents = [
            "Hello there",
            "Hi",
            "Hello hello",
            "Hey",
            "Hello hello",
            "Hi",
            "Hello",
            "Hi",
        ]
        with self.make_files(*contents) as filenames:
            self.assertSameMatches(
                find_duplicates([*filenames]),
                [
                    {filenames[1], filenames[5], filenames[7]},
                    {filenames[2], filenames[4]},
                ],
            )

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_compares_efficiently(self):
        contents = [
            bin(i)
            for i in range(248)
        ] + ["0b0", "0b1"]
        with self.make_files(*contents) as files:
            with Timer() as check:
                self.assertSameMatches(
                    find_duplicates(files),
                    [{files[0], files[-2]}, {files[1], files[-1]}],
                )
            self.assertLess(check.elapsed, 5, "Less than 5 seconds")
            with Timer() as t5:
                self.assertSameMatches(find_duplicates(files[:5]), [])
            with Timer() as t50:
                self.assertSameMatches(find_duplicates(files[:10]), [])
            self.assertLess(t50.elapsed, t5.elapsed*100)
            with Timer() as t250:
                self.assertSameMatches(
                    find_duplicates(files),
                    [{files[0], files[-2]}, {files[1], files[-1]}],
                )
            self.assertLess(t250.elapsed, t50.elapsed*300)
            self.assertLess(t250.elapsed, t5.elapsed*1000)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_even_more_efficient(self):
        contents = [
            "\xff" * i
            for i in reversed(range(100, 1000))
        ]
        contents.insert(0, contents[0])  # Duplicate last one
        with self.make_files(*contents[:75]) as files:
            with Timer() as check:
                self.assertSameMatches(
                    find_duplicates(files),
                    [{files[0], files[1]}],
                )
            self.assertLess(check.elapsed, 3, "Less than 3 seconds")
            times = []
            for _ in range(5):
                with Timer() as t5:
                    self.assertSameMatches(
                        find_duplicates(files[:5]),
                        [{files[0], files[1]}],
                    )
                times.append(t5.elapsed)
            t5_time = min(times)
            times = []
            for _ in range(5):
                with Timer() as t75:
                    self.assertSameMatches(
                        find_duplicates(files[:75]),
                        [{files[0], files[1]}],
                    )
                times.append(t75.elapsed)
            t75_time = min(times)
            self.assertLess(t75_time, t5_time*10)
            with self.make_files(*contents[75:250]) as more_files:
                self.assertSameMatches(
                    find_duplicates(files),
                    [{files[0], files[1]}],
                )
                files += more_files
                times = []
                for _ in range(5):
                    with Timer() as t250:
                        self.assertSameMatches(
                            find_duplicates(files[:250]),
                            [{files[0], files[1]}],
                        )
                    times.append(t250.elapsed)
                    t250_time = min(times)
                self.assertLess(t250_time, t5_time*50)
                with self.make_files(*contents[250:]) as more_files:
                    files += more_files
                    self.assertSameMatches(
                        find_duplicates(files),
                        [{files[0], files[1]}],
                    )
                    times = []
                    for _ in range(5):
                        with Timer() as t1000:
                            self.assertSameMatches(
                                find_duplicates(files[:1000]),
                                [{files[0], files[1]}],
                            )
                        times.append(t1000.elapsed)
                    t1000_time = min(times)
                    self.assertLess(t1000_time, t5.elapsed*150)


@contextmanager
def make_file(contents=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wb', delete=False) as f:
        if contents:
            if isinstance(contents, str):
                contents = contents.encode('utf-8')
            f.write(contents)
    try:
        yield str(Path(f.name).resolve())
    finally:
        os.remove(f.name)


class Timer:

    """Context manager to time a code block."""

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start


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
