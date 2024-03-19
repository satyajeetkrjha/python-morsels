import math
import unittest

from circle import Circle


class CircleTests(unittest.TestCase):

    """Tests for Circle."""

    def test_radius(self):
        circle = Circle(5)
        self.assertEqual(circle.radius, 5)

    def test_default_radius(self):
        circle = Circle()
        self.assertEqual(circle.radius, 1)

    def test_diameter(self):
        circle = Circle(2)
        self.assertEqual(circle.diameter, 4)

    def test_area(self):
        circle = Circle(2)
        self.assertEqual(circle.area, math.pi * 4)
        circle = Circle(1)
        self.assertEqual(circle.area, math.pi)

    def test_string_representation(self):
        circle = Circle(2)
        self.assertIn(str(circle), ['Circle(2)', 'Circle(2.0)'])
        self.assertIn(repr(circle), ['Circle(2)', 'Circle(2.0)'])
        circle.radius = 1
        self.assertIn(repr(circle), ['Circle(1)', 'Circle(1.0)'])

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_diameter_and_area_change_based_on_radius(self):
        circle = Circle(2)
        self.assertEqual(circle.diameter, 4)
        circle.radius = 3
        self.assertEqual(circle.diameter, 6)
        self.assertEqual(circle.area, math.pi * 9)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_diameter_changeable_but_area_not(self):
        circle = Circle(2)
        self.assertEqual(circle.diameter, 4)
        self.assertEqual(circle.area, math.pi * 4)
        circle.diameter = 3
        self.assertEqual(circle.radius, 1.5)
        with self.assertRaises(AttributeError):
            circle.area = 3

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_no_negative_radius(self):
        with self.assertRaises(ValueError) as context:
            circle = Circle(-2)
        self.assertEqual(
            str(context.exception).lower(),
            "radius cannot be negative",
        )
        circle = Circle(2)
        with self.assertRaises(ValueError) as context:
            circle.radius = -10
        self.assertEqual(
            str(context.exception).lower(),
            "radius cannot be negative",
        )
        with self.assertRaises(ValueError):
            circle.diameter = -20
        self.assertEqual(circle.radius, 2)


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
