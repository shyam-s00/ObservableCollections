import unittest

from reactive.ObservableList import ObservableList

class ObservableListMutationTests(unittest.TestCase):

    def setUp(self):
        self.emptyList = ObservableList()
        self.loadedList = ObservableList([1,2,3,4])

    def test_add_itemto_Observable_list(self):
        # arrange & act
        self.emptyList.append(1)
        self.loadedList.append(5)

        # assert
        self.assertEqual(len(self.emptyList), 1)
        self.assertEqual(len(self.loadedList), 5)

    def test_pop_removes_lastitem_inObservable_list(self):
        # arrange & act
        self.loadedList.pop()

        # asssert
        with self.assertRaises(IndexError):
            self.emptyList.pop()
        
        self.assertEqual(self.loadedList[-1], 3)

    def test_remove_removes_thevalue_passed(self):
        # arrange & act
        self.loadedList.remove(1)

        # assert        
        self.emptyList.remove(1) # This will not raise value error but push valueerror to on_error.
        self.loadedList.remove(5)        

        self.assertEqual(len(self.loadedList), 3)

    def test_insert_adds_theelement_at_position(self):
        # arrange & act
        self.emptyList.insert(1, 0)
        self.emptyList.insert(2, 2)
        
        self.loadedList.insert(5, 5)
        self.loadedList.insert(-1, 0)

        # assert
        self.assertEqual(len(self.emptyList), 2)
        self.assertEqual(len(self.loadedList), 6)
        self.assertEqual(self.loadedList, ObservableList([-1, 1, 2, 3, 4, 5]))

    def test_equality(self):
        # arrange 
        ol = ObservableList([1,2,3,4])

        # act & assert
        self.assertEqual(self.loadedList, ol)

    def test_extend_inserts_rangeof_values_tothe_list(self):
        # arrange
        ol = ObservableList([1,2,3,4])

        # act
        ol.extend([5,6,7,8])

        # assert
        self.assertEqual(8, len(ol))
        self.assertEqual(ObservableList([1,2,3,4,5,6,7,8]), ol)

    def test_sort_rearranges_elements_in_ascending(self):
        # arrange
        ol = ObservableList([5,1,2,6,4,3])

        # act
        ol.sort()

        # assert
        self.assertEqual(ObservableList([1,2,3,4,5,6]), ol)

    def test_sort_rearranges_elements_in_descending(self):
        # arrange
        ol = ObservableList([5,1,2,6,4,3])

        # act
        ol.sort(reverse=True)

        # assert
        self.assertEqual(ObservableList([6,5,4,3,2,1]), ol)

    def test_count_returns_count_ofelement_or_zero(self):
        # arrange
        self.loadedList.extend([1,2,3,4])

        # act
        count = self.loadedList.count(None)
        twoCount = self.loadedList.count(2)

        # assert
        self.assertEqual(0, count)
        self.assertEqual(2, twoCount)

    def test_clear_completely_removes_all_items_fromthe_list(self):
        # arrange
        self.loadedList.extend([5,6,7,8])

        # act
        self.loadedList.clear()
        self.emptyList.clear()

        # assert
        self.assertEqual(0, len(self.emptyList))
        self.assertEqual(0, len(self.loadedList))