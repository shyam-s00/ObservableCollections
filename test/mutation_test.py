import unittest

from ObservableList import ObservableList

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
        with self.assertRaises(ValueError):
            self.emptyList.remove(1)
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

