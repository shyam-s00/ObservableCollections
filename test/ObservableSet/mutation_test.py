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

    def test_clear_removes_all_items_from_ObservableSet(self):
        # arrange & act
        self.empty_os.clear()
        self.loaded_os.clear()

        # assert
        self.assertIsNotNone(self.empty_os)
        self.assertIsNotNone(self.loaded_os)
        self.assertEqual(len(self.empty_os), 0)
        self.assertEqual(len(self.loaded_os), 0)

    def test_update_with_another_ObservableSet_adds_items_toSource(self):
        # arrange & act
        self.empty_os.update({"a", "b", "c"})
        self.loaded_os.update(self.empty_os)

        # assert
        self.assertEqual(len(self.empty_os), 3)
        self.assertTrue("a" in self.empty_os)
        self.assertEqual(len(self.loaded_os), 7)
        self.assertTrue("c" in self.loaded_os)
        self.assertFalse({"a", "b", "c"} in self.loaded_os)

    def test_update_with_other_types_adds_items_to_ObservableSet(self):
        # arrange & act
        self.empty_os.update("abc")
        self.loaded_os.update([5, 6, 7, 8])

        # assert
        self.assertEqual(len(self.empty_os), 3)
        self.assertTrue("a" in self.empty_os)
        self.assertEqual(len(self.loaded_os), 8)
        self.assertTrue(7 in self.loaded_os)

    def test_discard_removes_the_element_passed_from_ObservableSet(self):
        # arrange & act
        self.empty_os.discard(4)
        self.loaded_os.discard(2)

        # assert
        self.assertEqual(len(self.empty_os), 0)
        self.assertEqual(len(self.loaded_os), 3)
        self.assertFalse(2 in self.loaded_os)

    def test_pop_removes_a_random_element_from_ObservableSet(self):
        # arrange & act
        nothing = self.empty_os.pop()
        out = self.loaded_os.pop()

        # assert
        self.assertIsNone(nothing)
        self.assertEqual(len(self.empty_os), 0)
        self.assertEqual(len(self.loaded_os), 3)
        self.assertIsNotNone(out)
        self.assertTrue(out not in self.loaded_os)

    def test_difference_returns_new_set_difference_of_two_ObservableSet(self):
        # arrange
        set_a = ObservableSet(("a", "b", "c", "d"))
        set_b = ObservableSet(("c", "d", "e"))

        # act
        out = set_a.difference(set_b)

        # assert
        self.assertEqual(set_a, ObservableSet(("a", "b", "c", "d")))
        self.assertEqual(set_b, ObservableSet(("c", "d", "e")))
        self.assertEqual(out, ObservableSet(('a', 'b')))

    def test_intersection_returns_new_set_intersection_of_two_or_more_ObservableSet(self):
        # arrange
        set_a = ObservableSet((2, 3, 5, 4))
        set_b = ObservableSet((2, 5, 100))
        set_c = ObservableSet((2, 3, 8, 9, 10))

        # act
        out_1 = set_b.intersection(set_a)
        out_2 = set_b.intersection(set_c)
        out_3 = set_a.intersection(set_c)
        out_4 = set_c.intersection(set_a, set_b)

        # assert
        self.assertEqual(out_1, ObservableSet((2, 5)))
        self.assertNotEqual(out_1, out_3)
        self.assertEqual(out_2, out_4)

    def test_symmetric_difference_returns_new_set_with_elements_not_in_both(self):
        # arrange
        set_a = ObservableSet((1, 2, 3, 4))
        set_b = ObservableSet((3, 4, 5))

        # act
        out_1 = set_b.symmetric_difference(set_a)
        out_2 = set_a.symmetric_difference(set_b)

        # assert
        self.assertEqual(out_2, out_1, ObservableSet((1, 2, 5)))

    def test_union_returns_new_set_with_distinct_elements_from_all_sets(self):
        # arrange
        set_a = ObservableSet((2, 3, 4))
        set_b = ObservableSet((3, 4, 5))
        set_c = ObservableSet((6, 7, 8))

        # act
        out_1 = set_a.union(set_b)
        out_2 = set_b.union(set_c, set_a)

        # assert
        self.assertEqual(out_1, ObservableSet((2, 3, 4, 5)))
        self.assertEqual(out_2, ObservableSet((2, 3, 4, 5, 6, 7, 8)))

    def test_isdisjoint_returns_true_or_false_for_two_ObservableSet(self):
        # arrange
        set_a = ObservableSet((1, 2, 3, 4))
        set_b = ObservableSet((5, 6, 7))
        set_c = ObservableSet((4, 5, 6))

        # act & assert
        self.assertTrue(set_a.isdisjoint(set_b))
        self.assertFalse(set_a.isdisjoint(set_c))

    def test_issubset_returns_true_or_false_for_two_ObservableSet(self):
        # arrange
        set_a = ObservableSet((1, 2, 3))
        set_b = ObservableSet((1, 2, 3, 4, 5))
        set_c = ObservableSet((1, 2, 4, 5))

        # act & assert
        self.assertTrue(set_a.issubset(set_b))
        self.assertFalse(set_b.issubset(set_a))
        self.assertTrue(set_c.issubset(set_b))
        self.assertFalse(set_a.issubset(set_c))

    def test_issuperset_returns_true_or_false_for_two_ObservableSet(self):
        # arrange
        set_a = ObservableSet((1, 2, 3, 4, 5))
        set_b = ObservableSet((1, 2, 3))
        set_c = ObservableSet((1, 2, 3))

        # act & assert
        self.assertTrue(set_a.issuperset(set_b))
        self.assertFalse(set_b.issuperset(set_a))
        self.assertTrue(set_c.issuperset(set_b))
        self.assertTrue(set_b.issuperset(set_c))

    def tearDown(self):
        self.empty_os.dispose()
        self.loaded_os.dispose()
