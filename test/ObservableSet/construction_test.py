import unittest

from reactive.ObservableSet import ObservableSet


class ObservableSetConstructionTest(unittest.TestCase):

    def test_ObservableSet_creation_without_items(self):
        # arrange & act
        os = ObservableSet()

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 0)

    def test_ObservableSet_creation_with_items(self):
        # arrange & act
        os = ObservableSet([1, 2, 3, 4])

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 4)

    def test_ObservableSet_creation_with_duplicate_items(self):
        # arrange & act
        os = ObservableSet([1, 2, 2, 3])

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 3)

    def test_ObservableSet_creation_with_a_normal_set(self):
        # arrange & act
        os = ObservableSet({1, 2, 2, 3})

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 3)

    def test_ObservableSet_creation_with_a_tuple(self):
        # arrange & act
        os = ObservableSet((1, 2, 3, 3, 2))

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 3)

    def test_ObservableSet_creation_with_mixed_data_types(self):
        # arrange & act
        os = ObservableSet({1, "2", "Three", (4, 5, 6), ("7", "Eight")})

        # assert
        self.assertIsNotNone(os)
        self.assertTrue(isinstance(os, ObservableSet))
        self.assertEqual(len(os), 5)

    def test_ObservableSet_creation_with_set_literal_containing_list_fails(self):
        # arrange, act & assert
        with self.assertRaises(TypeError):
            ObservableSet({"a", "b", ["c", "d"]})

    def test_equality_of_ObservableSet_with_set(self):
        # arrange
        normal_set = {1, 2, 3, 4}
        observable_set = ObservableSet((1, 2, 3, 4))

        # act & assert
        self.assertFalse(observable_set == normal_set)
        self.assertTrue(normal_set != observable_set)

    def test_iterable_protocol_of_ObservableSet(self):
        # arrange
        observable_set = ObservableSet((1, 2, 3, 4))

        # act
        i = iter(observable_set)

        # assert
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertEqual(next(i), 3)
        self.assertEqual(next(i), 4)
        self.assertRaises(StopIteration, lambda: next(i))
