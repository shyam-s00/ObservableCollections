import unittest

from reactive.ObservableSet import ObservableSet


class ObservableSetMutationTests(unittest.TestCase):

    def setUp(self):
        self.empty_os = ObservableSet()
        self.loaded_os = ObservableSet((1, 2, 3, 4))

    def test_add_single_item_to_ObservableSet(self):
        # arrange & act
        self.empty_os.add(1)
        self.loaded_os.add(5)

        # assert
        self.assertEqual(len(self.empty_os), 1)
        self.assertTrue(1 in self.empty_os)
        self.assertEqual(len(self.loaded_os), 5)
        self.assertTrue(5 in self.loaded_os)

    def test_add_iterable_of_different_type_to_ObservableSet(self):
        # arrange & act
        self.empty_os.add((1, 2, 2, "three"))
        self.loaded_os.add((5, 9))

        # assert
        self.assertEqual(len(self.empty_os), 1)
        self.assertFalse("three" in self.empty_os)
        self.assertTrue((1, 2, 2, "three") in self.empty_os)
        self.assertEqual(len(self.loaded_os), 5)
        self.assertTrue(5 not in self.loaded_os)

    def tearDown(self):
        self.empty_os.dispose()
        self.loaded_os.dispose()
