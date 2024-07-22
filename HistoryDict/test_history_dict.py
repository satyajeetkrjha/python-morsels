import unittest


from history_dict import HistoryDict


class HistoryDictTests(unittest.TestCase):

    """Tests for HistoryDict."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def assertHistoryEqual(self, mapping1, mapping2):
        self.assertEqual(
            {k: list(v) for k, v in mapping1.items()},
            {k: list(v) for k, v in mapping2.items()},
        )

    def test_initializing_with_dict(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        self.assertIterableEqual(counts.history("ducks"), [3])
        self.assertIterableEqual(counts.history("stickers"), [10])
        self.assertIterableEqual(counts.history("laptops"), [1])

    def test_initializing_with_iterable_of_tuples(self):
        counts = HistoryDict([
            ("ducks", 3),
            ("stickers", 10),
            ("laptops", 1),
        ])
        self.assertIterableEqual(counts.history("ducks"), [3])
        self.assertIterableEqual(counts.history("stickers"), [10])
        self.assertIterableEqual(counts.history("laptops"), [1])

    def test_adding_new_value(self):
        counts = HistoryDict()
        counts["ducks"] = 3
        self.assertIterableEqual(counts.history("ducks"), [3])

    def test_updating_values(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        counts["ducks"] = 5
        counts["laptops"] -= 1
        self.assertIterableEqual(counts.history("ducks"), [3, 5])
        self.assertIterableEqual(counts.history("stickers"), [10])
        self.assertIterableEqual(counts.history("laptops"), [1, 0])

    def test_setdefault(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        counts.setdefault("laptops", 1)
        counts.setdefault("cats", 1)
        self.assertIterableEqual(counts.history("ducks"), [3])
        self.assertIterableEqual(counts.history("stickers"), [10])
        self.assertIterableEqual(counts.history("laptops"), [1])
        self.assertIterableEqual(counts.history("cats"), [1])

    def test_update_method(self):
        counts = HistoryDict()
        counts.update({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        self.assertIterableEqual(counts.history("ducks"), [3])
        self.assertIterableEqual(counts.history("stickers"), [10])
        self.assertIterableEqual(counts.history("laptops"), [1])
        counts.update([("cats", 1), ("laptops", 0)])
        self.assertIterableEqual(counts.history("cats"), [1])
        self.assertIterableEqual(counts.history("laptops"), [1, 0])

    def test_repr(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        self.assertEqual(
            repr(counts),
            "HistoryDict({'ducks': 3, 'stickers': 10, 'laptops': 1})",
        )

    def test_keys_items_values(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        self.assertIterableEqual(
            counts.keys(),
            ["ducks", "stickers", "laptops"],
        )
        self.assertIterableEqual(
            counts.items(),
            [("ducks", 3), ("stickers", 10), ("laptops", 1)],
        )
        self.assertIterableEqual(counts.values(), [3, 10, 1])

    def test_equality(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        self.assertEqual(counts, {'ducks': 3, 'stickers': 10, 'laptops': 1})
        self.assertNotEqual(counts, {'ducks': 4, 'stickers': 10, 'laptops': 1})
        self.assertNotEqual(counts, {'ducks': 3, 'stickers': 10})
        self.assertEqual(counts, HistoryDict(counts))
        self.assertNotEqual(counts, None)
        self.assertNotEqual(counts, 4)
        self.assertNotEqual(counts, [])

    # To test bonus 1, comment out the next line
    @unittest.expectedFailure
    def test_deleting_keys(self):
        from history_dict import DELETED
        self.assertEqual(repr(DELETED), "DELETED")
        self.assertNotEqual(DELETED, "DELETED")

        counts = HistoryDict()
        counts.update({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })

        # pop method
        self.assertEqual(counts.pop("laptops"), 1)
        self.assertIterableEqual(counts.history("laptops"), [1, DELETED])
        self.assertIs(counts.history("laptops")[-1], DELETED)

        # del statement
        counts["laptops"] = 4
        del counts["laptops"]
        self.assertIterableEqual(counts.history("laptops"), [1, DELETED, 4, DELETED])

        # pop with default
        self.assertEqual(counts.pop("laptops", 0), 0)
        self.assertIterableEqual(counts.history("laptops"), [1, DELETED, 4, DELETED])

        # clear method
        self.assertIterableEqual(counts.history("ducks"), [3])
        self.assertIterableEqual(counts.history("stickers"), [10])
        counts.clear()
        self.assertIterableEqual(counts.history("ducks"), [3, DELETED])
        self.assertIterableEqual(counts.history("stickers"), [10, DELETED])

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_history_with_non_existant_key_and_all_history(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })

        # History with key that has never been assigned
        self.assertIterableEqual(counts.history("cats"), [])
        counts["cats"] = 1
        self.assertIterableEqual(counts.history("cats"), [1])
        self.assertIterableEqual(counts.history("squirrels"), [])

        # All history
        self.assertHistoryEqual(counts.all_history(), {
            "ducks": [3],
            "stickers": [10],
            "laptops": [1],
            "cats": [1],
        })
        counts["laptops"] += 1
        counts["stickers"] = 0
        self.assertHistoryEqual(counts.all_history(), {
            "ducks": [3],
            "stickers": [10, 0],
            "laptops": [1, 2],
            "cats": [1],
        })

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_immutable_views(self):
        counts = HistoryDict({
            "ducks": 3,
            "stickers": 10,
            "laptops": 1,
        })
        duck_history = counts.history("ducks")
        self.assertIterableEqual(duck_history, [3])
        all_history = counts.all_history()

        # Can't change the iterable
        with self.assertRaises(Exception):
            duck_history[0] = 1
        with self.assertRaises(Exception):
            duck_history.append(0)
        with self.assertRaises(Exception):
            duck_history.extend([1, 2])
        with self.assertRaises(Exception):
            duck_history.insert(0, 10)
        with self.assertRaises(Exception):
            duck_history.pop()
        with self.assertRaises(Exception):
            del duck_history[0]
        with self.assertRaises(Exception):
            duck_history.clear()
        self.assertIterableEqual(duck_history, [3])

        # The iterable updates whenever the dictionary updates
        counts["ducks"] = 2
        self.assertIterableEqual(duck_history, [3, 2])

        # All history is immutable also
        with self.assertRaises(Exception):
            all_history.pop("ducks")
        with self.assertRaises(Exception):
            del all_history["ducks"]
        with self.assertRaises(Exception):
            all_history["ducks"] = [5]
        with self.assertRaises(Exception):
            all_history.update({"ducks": [5]})
        with self.assertRaises(Exception):
            all_history.clear()
        with self.assertRaises(Exception):
            all_history["ducks"][0] = 1
        with self.assertRaises(Exception):
            all_history["ducks"].append(0)
        with self.assertRaises(Exception):
            all_history["ducks"].extend([1, 2])
        with self.assertRaises(Exception):
            all_history["ducks"].insert(0, 10)
        with self.assertRaises(Exception):
            all_history["ducks"].pop()
        with self.assertRaises(Exception):
            all_history["ducks"].clear()
        self.assertHistoryEqual(counts.all_history(), {
            "ducks": [3, 2],
            "stickers": [10],
            "laptops": [1],
        })

        # All history updates automatically too
        counts["ducks"] = 8
        self.assertHistoryEqual(counts.all_history(), {
            "ducks": [3, 2, 8],
            "stickers": [10],
            "laptops": [1],
        })
        self.assertIterableEqual(all_history["ducks"], [3, 2, 8])


if __name__ == "__main__":
    unittest.main(verbosity=2)
