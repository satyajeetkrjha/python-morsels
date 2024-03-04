import unittest


from easydict import EasyDict


class EasyDictTests(unittest.TestCase):

    """Tests for EasyDict."""

    def test_constructor(self):
        EasyDict()
        EasyDict({'a': 2, 'b': 3})

    def test_key_access(self):
        d = EasyDict({'a': 2, 'b': 3})
        self.assertEqual(d['a'], 2)
        self.assertEqual(d['b'], 3)

    def test_attribute_access(self):
        d = EasyDict({'a': 2, 'b': 3})
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)

    def test_original_dictionary_unchanged(self):
        mapping = {'a': 2, 'b': 3}
        d = EasyDict(mapping)
        d.c = 4
        self.assertEqual(mapping, {'a': 2, 'b': 3})

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_allow_setting_keys_and_attributes(self):
        d = EasyDict({'a': 2, 'b': 3})
        d['a'] = 4
        self.assertEqual(d['a'], 4)
        self.assertEqual(d.a, 4)
        d.c = 9
        self.assertEqual(d['c'], 9)
        self.assertEqual(d.c, 9)
        self.assertEqual(d['b'], 3)
        x = EasyDict()
        y = EasyDict()
        x.a = 4
        y.a = 5
        self.assertEqual(x.a, 4)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_keyword_arguments_equality_and_get_method(self):
        d = EasyDict(a=2, b=3, c=4, d=5)
        self.assertEqual(d.a, 2)
        self.assertEqual(d.b, 3)
        self.assertEqual(d['c'], 4)
        self.assertEqual(d['d'], 5)
        x = EasyDict({'a': 2, 'b': 3})
        y = EasyDict({'a': 2, 'b': 4})
        self.assertNotEqual(x, y)
        y.b = 3
        self.assertEqual(x, y)
        x.c = 5
        self.assertNotEqual(x, y)
        y.c = 5
        self.assertEqual(x, y)
        self.assertIsNone(y.get('d'))
        self.assertEqual(y.get('c'), 5)
        self.assertEqual(y.get('d', 5), 5)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_normalize_arg(self):
        d = EasyDict({'greeting 1': 'hi'}, normalize=True)
        self.assertEqual(d['greeting 1'], 'hi')
        self.assertEqual(d.greeting_1, 'hi')
        d.greeting_2 = 'hello'
        self.assertEqual(d['greeting 2'], 'hello')
        self.assertEqual(d.greeting_2, 'hello')
        d['greeting 2'] = 'hey'
        self.assertEqual(d['greeting 2'], 'hey')
        self.assertEqual(d.get('greeting 2'), 'hey')
        self.assertEqual(d.greeting_2, 'hey')
        with self.assertRaises(AttributeError):
            d.greeting2
        d = EasyDict({'greeting 1': 'hi'})
        self.assertEqual(d['greeting 1'], 'hi')
        with self.assertRaises(AttributeError):
            d.greeting_1


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
