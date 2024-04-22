from io import StringIO
import unittest

from call_later import call_later


class CallLaterTests(unittest.TestCase):

    """Tests for call_later."""

    def test_append_to_list(self):
        names = []
        append_name = call_later(names.append, "Trey")
        self.assertIsNone(append_name())
        self.assertEqual(names, ['Trey'])
        append_name()
        self.assertEqual(names, ['Trey', 'Trey'])

    def test_zip_later(self):
        call_zip = call_later(zip, [1, 2], [3, 4])
        self.assertEqual(list(call_zip()), [(1, 3), (2, 4)])

    def test_print_with_positional_and_keyword_arguments(self):
        f = StringIO()
        print123 = call_later(print, 1, 2, 3, sep=", ", end="!\n", file=f)
        self.assertEqual(print123(), None)
        self.assertEqual(f.getvalue(), "1, 2, 3!\n")
        print123 = call_later(print, 1, 2, 3, sep=", ", end="!\n", file=f)
        self.assertEqual(print123(), None)
        self.assertEqual(f.getvalue(), "1, 2, 3!\n1, 2, 3!\n")


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2)

