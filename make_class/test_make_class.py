import unittest


from make_class import make_class


class MakeClassTests(unittest.TestCase):

    """Tests for make_class class factory."""

    def test_class_name(self):
        Point = make_class('Point', ['x', 'y'])
        self.assertEqual(type(Point), type)
        self.assertRegex(str(Point), r"^<class '[^']*Point'>$")

    def test_keyword_arguments(self):
        Point = make_class('Point', ['x', 'y'])
        p = Point(x=1, y=2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        q = Point(y=1, x=2)
        self.assertEqual(q.x, 2)
        self.assertEqual(q.y, 1)

    def test_position_arguments(self):
        Point = make_class('Point', ['x', 'y'])
        p = Point(1, 2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_arguments_as_one_string(self):
        Person = make_class('Person', 'name favorite_color')
        trey = Person("Trey", "purple")
        self.assertEqual(trey.name, "Trey")
        self.assertEqual(trey.favorite_color, "purple")

    def test_invalid_arguments(self):
        make_class('Person', 'name1 favorite_col0r')
        with self.assertRaises(ValueError):
            make_class('Person', '1name favorite_col0r')
        with self.assertRaises(ValueError):
            make_class('Person', 'name1 favorite-col0r')
        with self.assertRaises(ValueError):
            make_class('Person', 'name1 favorite-col0r')
        with self.assertRaises(ValueError):
            make_class('Person', 'name1 fav.color')

    def test_missing_arguments(self):
        Person = make_class('Person', 'name favorite_color')
        with self.assertRaises(TypeError):
            Person("Trey")
        with self.assertRaises(TypeError):
            Person(favorite_color="purple")
        with self.assertRaises(TypeError):
            Person(name="Trey")

    def test_too_many_arguments(self):
        Person = make_class('Person', 'name')
        trey = Person("Trey")
        self.assertEqual(trey.name, "Trey")
        with self.assertRaises(TypeError):
            Person("Trey", favorite_color="purple")
        with self.assertRaises(TypeError):
            Person("Trey", "purple")

    def test_multiple_classes(self):
        classes = [
            make_class('A', ['a']),
            make_class('B', ['a', 'b']),
            make_class('C', ['a', 'b', 'c']),
            make_class('D', ['a', 'b', 'c', 'd']),
        ]
        objects = [
            cls(*range(n))
            for n, cls in enumerate(classes, start=1)
        ]
        self.assertEqual(objects[0].a, 0)
        self.assertEqual(objects[1].a, 0)
        self.assertEqual(objects[2].a, 0)
        self.assertEqual(objects[3].a, 0)
        self.assertEqual(objects[1].b, 1)
        self.assertEqual(objects[2].b, 1)
        self.assertEqual(objects[3].b, 1)
        self.assertEqual(objects[2].c, 2)
        self.assertEqual(objects[3].c, 2)
        self.assertEqual(objects[3].d, 3)

    def test_string_representation(self):
        Point = make_class('Point', ['x', 'y'])
        p = Point(3, 4)
        q = Point(y=5, x=6)
        self.assertEqual(str(p), "Point(x=3, y=4)")
        self.assertEqual(repr(q), "Point(x=6, y=5)")

        ColoredPoint = make_class('ColoredPoint', ['x', 'y', 'color'])
        p = ColoredPoint(3, 4, 'purple')
        q = ColoredPoint(y=5, x=6, color='green')
        self.assertEqual(str(p), "ColoredPoint(x=3, y=4, color='purple')")
        self.assertEqual(repr(q), "ColoredPoint(x=6, y=5, color='green')")

    def test_string_representation_with_inheritance(self):
        BasePoint = make_class('BasePoint', ['x', 'y'])
        class Point(BasePoint):
            def __init__(self, x, y, color=None):
                super().__init__(x, y)
                self.color = color
            @classmethod
            def origin(cls, color=None):
                return cls(0, 0, color=color)

        Point.__qualname__ = Point.__name__
        p = Point.origin('purple')
        self.assertEqual((p.x, p.y), (0, 0))
        self.assertEqual(p.color, 'purple')
        self.assertEqual(repr(p), "Point(x=0, y=0)")

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_equality(self):
        Point = make_class('Point', ['x', 'y'])
        Point2 = make_class('Point', ['x', 'y'])
        self.assertNotEqual(Point(3, 4), Point(5, 6))
        self.assertEqual(Point(3, 4), Point(x=3, y=4))
        self.assertNotEqual(Point(3, 4), Point(4, 3))
        self.assertNotEqual(Point(3, 4), Point(3, 6))
        self.assertNotEqual(Point(3, 4), (3, 4))
        self.assertNotEqual(Point(3, 4), Point2(3, 4))

        class OtherClass:
            def __eq__(self, other):
                return True
        self.assertEqual(Point(3, 4), OtherClass())

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_restrict_attrs(self):
        Point = make_class('Point', ['x', 'y'], restrict_attrs=True)
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        p.x = 4
        self.assertEqual(p.x, 4)
        with self.assertRaises(AttributeError):
            p.z = 5
        with self.assertRaises(AttributeError):
            p.z
        Point2 = make_class('Point', ['x', 'y'], restrict_attrs=False)
        p = Point2(3, 4)
        p.z = 5
        self.assertEqual(p.z, 5)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_frozen(self):
        # Frozen without restricted attributes
        Point = make_class('Point', ['x', 'y'], frozen=True)
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        with self.assertRaises(Exception):
            p.x = 4
        self.assertEqual(p.x, 3)
        with self.assertRaises(Exception):
            p.z = 5
        self.assertEqual(p.__dict__, {'x': 3, 'y': 4})

        # Frozen with restricted attributes
        Point = make_class('Point', ['x', 'y'], frozen=True, restrict_attrs=True)
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        with self.assertRaises(Exception):
            p.x = 4
        self.assertEqual(p.x, 3)
        with self.assertRaises(Exception):
            p.z = 5
        with self.assertRaises(AttributeError):
            p.__dict__


if __name__ == "__main__":
    unittest.main(verbosity=2)
