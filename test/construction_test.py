import unittest
from reactive.ObservableList import ObservableList


class CollectionConstructionTests(unittest.TestCase):

    def test_when_observable_list_is_created_without_items(self):
        ol = ObservableList()
        self.assertIsNotNone(ol)
        self.assertEqual(len(ol), 0)

    def test_when_observablelist_is_created_with_items(self):
        ol = ObservableList([1, 2, 3, 4])
        self.assertIsNotNone(ol)
        self.assertEqual(len(ol), 4)

    def test_when_observablelist_is_with_items_checkfor_anitem(self):
        ol = ObservableList([1, 2, 3, 4])
        self.assertEqual(ol.index(2), 1)