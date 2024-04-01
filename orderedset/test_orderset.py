from collections.abc import Mapping, Iterable
from functools import partial
from itertools import islice
from sys import getsizeof
from textwrap import dedent
import timeit
import unittest


from orderedset import OrderedSet


class OrderedSetTests(unittest.TestCase):

    """Tests for OrderedSet."""

    def test_constructor_with_iterables(self):
        OrderedSet([1, 2, 3, 4])
        OrderedSet(n**2 for n in [1, 2, 3])

    def test_constructor_with_nothing(self):
        OrderedSet()

    def test_string_representations(self):
        numbers = OrderedSet(n**2 for n in [1, 2, 3, 4])
        empty = OrderedSet()
        self.assertEqual(str(numbers), "OrderedSet([1, 4, 9, 16])")
        self.assertEqual(repr(empty), "OrderedSet([])")

    def test_iterable(self):
        numbers = OrderedSet([1, 2, 3, 4])
        self.assertEqual(set(numbers), {1, 2, 3, 4})

    def test_uniqueness(self):
        numbers = OrderedSet([1, 3, 2, 4, 2, 1, 4, 5])
        self.assertEqual(sorted(numbers), [1, 2, 3, 4, 5])

    def test_maintains_order_and_uniqueness(self):
        string = "Hello world.  This string contains many characters in it."
        expected = "Helo wrd.Thistngcamy"
        characters = OrderedSet(string)
        self.assertEqual("".join(characters), expected)

    def test_length(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertEqual(len(numbers), 4)
        self.assertEqual(len(OrderedSet('hiya')), 4)
        self.assertEqual(len(OrderedSet('hello there')), 7)

    def test_containment(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertIn(2, numbers)
        self.assertNotIn(3, numbers)

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_memory_and_time_efficient(self):
        # Time efficient construction
        same = [9999 for _ in range(700)]
        different = [9999 + i for i in range(700)]
        time = partial(
            timer,
            globals={**globals(), "same": same, "different": different},
            number=30,
        )
        small_set_time = time("OrderedSet(same)")
        large_set_time = time("OrderedSet(different)")
        self.assertGreater(small_set_time*100, large_set_time)

        # Memory efficient
        numbers = OrderedSet([9999 for _ in range(2500)])
        numbers2 = OrderedSet([9999 + i for i in range(2500)])
        self.assertLess(get_size(numbers)*10, get_size(numbers2))
        self.assertLess(get_size(numbers), 3000)

        # Time efficient lookups
        first = next(iter(numbers2))
        last = next(islice(numbers2, 2499))
        time = partial(timer, globals=locals(), number=6000)
        beginning_lookup = time("assert first in numbers2")
        end_lookup = time("assert last in numbers2")
        not_in_lookup = time("assert 20_000 not in numbers2")
        self.assertGreater(beginning_lookup*50, end_lookup)
        self.assertGreater(end_lookup*50, beginning_lookup)
        self.assertGreater(beginning_lookup*50, not_in_lookup)
        self.assertGreater(end_lookup*50, not_in_lookup)
        self.assertGreater(not_in_lookup*50, end_lookup)
        self.assertGreater(not_in_lookup*50, beginning_lookup)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_equality(self):
        self.assertEqual(OrderedSet('abc'), OrderedSet('abc'))
        self.assertNotEqual(OrderedSet('abc'), OrderedSet('bac'))
        self.assertNotEqual(OrderedSet('abc'), OrderedSet('abcd'))
        self.assertEqual(OrderedSet('abc'), set('abc'))
        self.assertEqual(OrderedSet('bac'), set('abc'))
        self.assertNotEqual(OrderedSet('abc'), 'abc')
        self.assertNotEqual(OrderedSet('abc'), ['a', 'b', 'c'])

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_add_and_discard(self):
        numbers = OrderedSet([1, 2, 3])
        numbers.add(3)
        self.assertEqual(len(numbers), 3)
        numbers.add(4)
        self.assertEqual(len(numbers), 4)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)

        # Check for add method efficiency
        setup = "numbers = OrderedSet([])"
        time = partial(timer, setup=setup, globals=globals(), number=20)
        small_set_time = time(dedent("""
            add = numbers.add
            for n in [9999 for _ in range(700)]:
                add(n)
        """))
        large_set_time = time(dedent("""
            add = numbers.add
            for n in [9999 + i for i in range(700)]:
                add(n)
        """))
        self.assertGreater(small_set_time*100, large_set_time)


def timer(code, globals, number, repeat=5, setup=""):
    return min(timeit.repeat(
        code,
        number=number,
        repeat=repeat,
        globals=globals,
        setup=setup,
    ))


def get_size(obj, seen=None):
    """Return size of any Python object."""
    if seen is None:
        seen = set()
    size = getsizeof(obj)
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    if hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    if hasattr(obj, '__slots__'):
        size += sum(
            get_size(getattr(obj, attr), seen)
            for attr in obj.__slots__
            if hasattr(obj, attr)
        )
    if isinstance(obj, Mapping):
        size += sum(
            get_size(k, seen) + get_size(v, seen)
            for k, v in obj.items()
        )
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        size += sum(get_size(item, seen) for item in obj)
    return size


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
