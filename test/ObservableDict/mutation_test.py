import unittest

from reactive.ObservableDict import ObservableDict


class ObservableDictMutationTests(unittest.TestCase):

    def setUp(self):
        self.od = ObservableDict({1: 'Crash', 2: 'Coco', 3: 'Pura', 4: 'Tiny Tiger'})
        self.empty = ObservableDict()

    def test_ObservableDict_get_method_returns_appropriately(self):
        # arrange & act
        va11 = self.od.get(1)
        val2 = self.od.get(5)
        va13 = self.od.get(5, 'Dingo')

        # assert
        self.assertEqual(len(self.od), 4)
        self.assertTrue(va11 == 'Crash')
        self.assertIsNone(val2)
        self.assertIsNotNone(va13)
        self.assertEqual(va13, 'Dingo')

    def test_ObservableDict_get_with_index_access(self):
        # arrange
        val1 = self.od[1]

        # act & assert
        self.assertEqual(val1, 'Crash')

        with self.assertRaises(KeyError):
            # noinspection PyUnusedLocal
            value = self.od[5]

    def test_ObservableDict_del_a_value_or_entire_dict(self):
        # arrange & act
        del self.od[2]

        # assert
        self.assertEqual(len(self.od), 3)
        self.assertIsNone(self.od.get(2))

    def test_ObservableDict_items_returns_items_as_key_value_pair(self):
        # arrange & act
        items = self.od.items()

        # assert
        self.assertIsNotNone(items)
        self.assertEqual(len(items), 4)

    def test_ObservableDict_del_deletes_entire_dictionary_and_calls_dispose(self):
        # arrange
        local_dict = ObservableDict({1: 'hello', 2: 'world'})

        # act
        del local_dict

        # assert
        with self.assertRaises(UnboundLocalError):
            self.assertIsNone(local_dict)

    def test_ObservableDict_pop_removes_the_items_with_key_specified_and_returns_its_value(self):
        # arrange & act
        val1 = self.od.pop(4)
        val2 = self.od.pop(5, 'Dr. Neo Cortex')

        # assert
        self.assertEqual(len(self.od), 3)
        self.assertEqual(val1, 'Tiny Tiger')
        self.assertEqual(val2, 'Dr. Neo Cortex')

    def test_ObservableDict_popitem_removes_random_value(self):
        # arrange & act
        val1 = self.od.popitem()

        # assert
        self.assertIsNotNone(val1)
        self.assertEqual(len(self.od), 3)

    def test_ObservableDict_set_default_does_nothing_when_key_exists(self):
        # arrange & act
        val1 = self.od.setdefault(1)
        val2 = self.od.setdefault(2, 'Dingo')

        # assert
        self.assertIsNotNone(val1)
        self.assertEqual(val1, 'Crash')
        self.assertIsNotNone(val2)
        self.assertEqual(val2, 'Coco')

    def test_ObservableDict_set_default_creates_new_key_if_not_exists(self):
        # arrange & act
        val1 = self.od.setdefault(5, 'Dingo')
        val2 = self.od.setdefault(6)

        # assert
        self.assertIsNotNone(val1)
        self.assertEqual(val1, 'Dingo')
        self.assertIsNone(val2)

    def test_ObservableDict_fromkeys_creates_new_ObservableDict(self):
        # arrange & act
        new_dict = ObservableDict.fromkeys({1, 2, 3, 4, 5})

        # assert
        self.assertIsNotNone(new_dict)
        self.assertTrue(isinstance(new_dict, ObservableDict))
        self.assertEqual(len(new_dict), 5)

    def test_ObservableDict_clear_removes_all_items_in_dictionary(self):
        # arrange & act
        self.od.clear()

        # assert
        self.assertIsNotNone(self.od)
        self.assertEqual(len(self.od), 0)

    def tearDown(self):
        self.od.dispose()
        self.empty.dispose()
