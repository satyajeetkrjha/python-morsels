import math
import unittest


class TestNoStar(unittest.TestCase):

    """Tests for nostar module."""

    def test_no_star_import_allowed(self):
        with self.assertRaises(ImportError):
            # exec avoids SyntaxError https://discuss.python.org/t/21547
            exec("from nostar import *")

    def test_from_import_allowed(self):
        from nostar import tau
        self.assertEqual(tau, math.tau)

    def test_whole_model_import_allowed(self):
        import nostar
        self.assertEqual(nostar.tau, math.tau)


if __name__ == "__main__":
    import sys
    from platform import python_version
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2)
