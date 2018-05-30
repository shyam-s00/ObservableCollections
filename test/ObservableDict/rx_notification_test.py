import unittest

from rx.testing import TestScheduler, ReactiveTest
from rx.internal import DisposedException

from reactive.ObservableDict import ObservableDict
from reactive.shared.CollectionChangeAction import CollectionChangeAction

on_next = ReactiveTest.on_next
on_error = ReactiveTest.on_error


class RxNotificationObservableDictTest(unittest.TestCase):

    def setUp(self):
        self.od = ObservableDict({1: 'Crash', 2: 'Coco', 3: 'Pura', 4: 'Tiny'})
        self.scheduler = TestScheduler()

    def test_ObservableDict_elements_deleted_with_del_keyword(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_message = [on_next(0, 2)]

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        del self.od[2]

        # assert
        self.assertEqual(obs.messages, expected_message)
        self.assertEqual(len(self.od), 3)
        self.assertIsNone(self.od.get(2))

    def test_ObservableDict_del_keyword_with_invalid_key(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_error = [on_error(0, KeyError(5))]

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        del self.od[5]

        # assert
        self.assertEqual(obs.messages, expected_error)

    def test_ObservableDict_pop_with_invalid_key(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_message = [on_next(0, 'Coco'), on_error(0, KeyError(5))]

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.od.pop(2)
        self.od.pop(5)
        self.od.pop(3)

        # assert
        self.assertEqual(obs.messages, expected_message)
        self.assertEqual(len(self.od), 2)   # TODO: Re-visit here to see if this is valid. ???

    def test_ObservableDict_popitem_removes_arbitrary_value(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.od.popitem()
        self.od.popitem()

        # assert
        self.assertEqual(len(self.od), 2)
        self.assertEqual(len(obs.messages), 2)

    def test_ObservableDict_popitem_in_empty_dict_pushes_KeyError_in_on_error(self):
        # arrange
        obs = self.scheduler.create_observer()
        empty = ObservableDict()
        expected_error = [on_error(0, KeyError('popitem(): dictionary is empty'))]

        empty.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        empty.popitem()

        # assert
        self.assertEqual(obs.messages, expected_error)

    def test_ObservableDict_test_default_adds_key_if_not_exists(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.od.when_collection_changes() \
            .subscribe(obs)

        # act
        self.od.setdefault(5, 'Dingo')
        self.od.setdefault(6)

        # assert
        self.assertEqual(len(self.od), 6)
        self.assertEqual(len(obs.messages), 2)
        self.assertEqual(obs.messages[0].value.value.Items, 'Dingo')
        self.assertEqual(obs.messages[0].value.value.Action, CollectionChangeAction.ADD)
        self.assertEqual(obs.messages[1].value.value.Items, ())
        self.assertEqual(obs.messages[1].value.value.Action, CollectionChangeAction.ADD)

    def test_ObservableDict_test_default_does_nothing_key_if_exists(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_message = []

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.od.setdefault(2, 'Dingo')
        self.od.setdefault(1)

        # assert
        self.assertEqual(len(self.od), 4)
        self.assertEqual(len(obs.messages), 0)
        self.assertEqual(obs.messages, expected_message)

    def test_ObservableDict_update_method_updates_existing_dictionary(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_values = ['Polar', 'Dingo']

        self.od.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.od.update(ObservableDict({2: 'Polar', 5: 'Dingo'}))

        # assert
        self.assertEqual(len(self.od), 5)
        self.assertEqual(self.od.get(2), 'Polar')
        self.assertTrue(isinstance(obs.messages[0].value.value, ObservableDict))
        self.assertEqual(list(obs.messages[0].value.value._dict.values()), expected_values)

    def test_ObservableDict_clear_removes_all_items_and_publish_clear_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.od.when_collection_changes() \
            .subscribe(obs)

        # act
        self.od.clear()

        # assert
        self.assertEqual(len(self.od), 0)
        self.assertEqual(len(obs.messages), 1)
        self.assertEqual(obs.messages[0].value.value.Items, ())
        self.assertEqual(obs.messages[0].value.value.Action, CollectionChangeAction.CLEAR)

    def test_ObservableSet_with_any_operation_after_dispose_throws_DisposedException(self):
        # arrange
        obs = self.scheduler.create_observer()
        new_dict = ObservableDict({6: 'Polar', 5: 'Dingo'})

        new_dict.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act & assert
        new_dict.dispose()
        with self.assertRaises(DisposedException):
            new_dict.setdefault(6)

    def tearDown(self):
        self.od.dispose()
