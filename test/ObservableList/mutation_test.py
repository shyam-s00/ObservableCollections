import unittest

from reactive.ObservableList import ObservableList


class ObservableListMutationTests(unittest.TestCase):

    def setUp(self):
        self.emptyList = ObservableList()
        self.loadedList = ObservableList([1, 2, 3, 4])

    def test_add_itemTo_Observable_list(self):
        # arrange & act
        self.loadedList.append(5)
        self.emptyList.append(1)

        # assert
        self.assertEqual(len(self.emptyList), 1)
        self.assertEqual(len(self.loadedList), 5)

    def test_pop_removes_last_item_inObservable_list(self):
        # arrange & act
        self.loadedList.pop()

        # assert
        with self.assertRaises(IndexError):
            self.emptyList.pop()

        self.assertEqual(self.loadedList[-1], 3)

    def test_remove_removes_the_value_passed(self):
        # arrange & act
        self.loadedList.remove(1)

        # assert        
        self.emptyList.remove(1)  # This will not raise value error but push ValueError to on_error.
        self.loadedList.remove(5)

        self.assertEqual(len(self.loadedList), 3)

    def test_insert_adds_the_element_at_position(self):
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
        ol = ObservableList([1, 2, 3, 4])

        # act & assert
        self.assertEqual(self.loadedList, ol)

    def test_extend_inserts_rangeOf_values_to_the_list(self):
        # arrange
        ol = ObservableList([1, 2, 3, 4])

        # act
        ol.extend([5, 6, 7, 8])

        # assert
        self.assertEqual(8, len(ol))
        self.assertEqual(ObservableList([1, 2, 3, 4, 5, 6, 7, 8]), ol)

    def test_sort_rearranges_elements_in_ascending(self):
        # arrange
        ol = ObservableList([5, 1, 2, 6, 4, 3])

        # act
        ol.sort()

        # assert
        self.assertEqual(ObservableList([1, 2, 3, 4, 5, 6]), ol)

    def test_sort_rearranges_elements_in_descending(self):
        # arrange
        ol = ObservableList([5, 1, 2, 6, 4, 3])

        # act
        ol.sort(reverse=True)

        # assert
        self.assertEqual(ObservableList([6, 5, 4, 3, 2, 1]), ol)

    def test_count_returns_count_of_element_or_zero(self):
        # arrange
        self.loadedList.extend([1, 2, 3, 4])

        # act
        count = self.loadedList.count(None)
        two_count = self.loadedList.count(2)

        # assert
        self.assertEqual(0, count)
        self.assertEqual(2, two_count)

    def test_clear_completely_removes_all_items_from_the_list(self):
        # arrange
        self.loadedList.extend([5, 6, 7, 8])

        # act
        self.loadedList.clear()
        self.emptyList.clear()

        # assert
        self.assertEqual(0, len(self.emptyList))
        self.assertEqual(0, len(self.loadedList))

    def test_concat_operator_on_combines_two_ObservableList(self):
        # arrange
        new_list = ObservableList([5, 6, 7, 8])
        expected_output = ObservableList([1, 2, 3, 4, 5, 6, 7, 8])

        # act
        self.emptyList += new_list
        self.loadedList += new_list

        # assert
        self.assertEqual(new_list, self.emptyList)
        self.assertEqual(expected_output, self.loadedList)

    def test_ObservableList_item_membership(self):
        # arrange & act
        self.loadedList.extend([6, 7, 8, 9])

        # assert
        self.assertTrue(1 in self.loadedList)
        self.assertTrue(6 in self.loadedList)
        self.assertTrue(5 not in self.loadedList)

    def test_concat_operator_on_adding_list_with_ObservableList(self):
        # arrange
        ol = ObservableList([1, 2, 3, 4])
        nl = [5, 6, 7, 8]

        # act & assert
        self.assertRaises(TypeError, lambda: ol + nl)

    def tearDown(self):
        self.emptyList.dispose()
        self.loadedList.dispose()
