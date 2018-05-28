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
        # arrange
        od = ObservableDict({1: 'Tom', 2: 'Jerry'})

        # assert
        self.assertIsNotNone(od)
        self.assertTrue(isinstance(od, ObservableDict))
        self.assertEqual(len(od), 2)

    def test_ObservableDict_with_mixed_keys(self):
        # arrange
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
