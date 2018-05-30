import unittest

from reactive.ObservableDict import ObservableDict


class ObservableDictionaryConstructionTests(unittest.TestCase):

    def test_when_empty_ObservableDict_is_created(self):
        # arrange & act
        od = ObservableDict()

        # assert
        self.assertIsNotNone(od)
        self.assertTrue(isinstance(od, ObservableDict))
        self.assertEqual(len(od), 0)

    def test_ObservableDict_with_integer_keys(self):
        # arrange & act
        od = ObservableDict({1: 'Tom', 2: 'Jerry'})

        # assert
        self.assertIsNotNone(od)
        self.assertTrue(isinstance(od, ObservableDict))
        self.assertEqual(len(od), 2)

    def test_ObservableDict_with_mixed_keys(self):
        # arrange & act
        od = ObservableDict({'name': 'Tom', 1: 'Jerry', 'ids': [1, 2, 3]})

        # assert
        self.assertIsNotNone(od)
        self.assertTrue(isinstance(od, ObservableDict))
        self.assertEqual(len(od), 3)

    def test_ObservableDict_with_duplicate_integer_keys_raises_error(self):
        # arrange, act & assert
        with self.assertRaises(TypeError):
            od = ObservableDict({[1, 2]: 'Hello'})
            self.assertIsNone(od)

    def test_equality_of_ObservableDict_with_another(self):
        # arrange
        normal_dict = dict({1: 'Crash Bandicoot', 2: 'Neo Cortex'})
        observable_dict = ObservableDict({1: 'Crash Bandicoot', 2: 'Neo Cortex'})

        # act & assert
        self.assertTrue(observable_dict == ObservableDict({1: 'Crash Bandicoot', 2: 'Neo Cortex'}))
        self.assertFalse(observable_dict == normal_dict)
        self.assertTrue(observable_dict != normal_dict)
        self.assertFalse(observable_dict != ObservableDict(normal_dict))

    def test_membership_of_ObservableDict(self):
        # arrange
        observable_dict = ObservableDict({1: 'Crash Bandicoot', 2: 'Neo Cortex'})

        # act & assert
        self.assertTrue(1 in observable_dict)
        self.assertFalse(3 in observable_dict)

    def test_Iterable_protocol_of_ObservableDict(self):
        # arrange
        observable_dict = ObservableDict({1: 'Crash Bandicoot', 2: 'Neo Cortex'})

        # act
        i = iter(observable_dict)

        # assert
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_ObservableDict_values_returns_view_of_values(self):
        # arrange
        observable_dict = ObservableDict({1: 'Crash Bandicoot', 2: 'Neo Cortex'})

        # act
        val = observable_dict.values()

        # assert
        self.assertIsNotNone(val)
        self.assertEqual(len(val), 2)
