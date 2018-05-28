import unittest

from rx.internal import DisposedException

from reactive.ObservableList import ObservableList


class CollectionConstructionTests(unittest.TestCase):

    def test_when_observable_list_is_created_without_items(self):
        # arrange & act
        ol = ObservableList()

        # assert
        self.assertIsNotNone(ol)
        self.assertEqual(len(ol), 0)

    def test_when_ObservableList_is_created_with_items(self):
        # arrange & act
        ol = ObservableList([1, 2, 3, 4])

        # assert
        self.assertIsNotNone(ol)
        self.assertEqual(len(ol), 4)

    def test_when_ObservableList_is_with_items_check_for_an_item(self):
        # arrange & act
        ol = ObservableList([1, 2, 3, 4])

        # assert
        self.assertEqual(ol.index(2), 1)

    def test_equality_of_ObservableList(self):
        # arrange & act
        normal_list = [1, 2, 3, 4]
        ol1 = ObservableList(normal_list)
        ol2 = ObservableList([1, 2, 3, 4])
        ol3 = ObservableList([1, 2, 3, 4, 5])

        # assert
        self.assertEqual(ol1, ol2)
        self.assertFalse(ol1 == normal_list)
        self.assertNotEqual(ol1, ol3)
        self.assertTrue(ol3 != normal_list)

    def test_disposed_list_cannot_be_used_further(self):
        # arrange
        ol = ObservableList([1, 2, 3, 4])

        # act
        ol.dispose()

        # assert
        with self.assertRaises(DisposedException):
            ol.append(5)

    def test_ObservableList_index_access(self):
        # arrange
        ol = ObservableList([1, 2, 3, 4, -1, 6, 7, -2])

        # act & assert
        self.assertEqual(3, ol[2])
        self.assertEqual(-2, ol[-1])
        self.assertEqual(1, ol[0])

    def test_ObservableList_slicing_returns_list_slice(self):
        # arrange
        ol = ObservableList([1, 3, 5, 7, 9])

        # act & assert
        self.assertEqual(ObservableList([1, 3]), ol[:2])
        self.assertEqual(ObservableList([5, 7]), ol[2:4])
        self.assertEqual(ObservableList([1, 3, 5, 7, 9]), ol[:])
        self.assertEqual(ObservableList([3, 5, 7]), ol[-4:-1])

    def test_ObservableList_iterable_protocol(self):
        # arrange
        ol = ObservableList([1, 3, 5])

        # act
        i = iter(ol)

        # assert
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 3)
        self.assertEqual(next(i), 5)
        self.assertRaises(StopIteration, lambda: next(i))
