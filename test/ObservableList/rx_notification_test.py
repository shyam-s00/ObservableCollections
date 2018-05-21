import unittest

from rx.testing import ReactiveTest, TestScheduler

from reactive.shared.CollectionChangeAction import CollectionChangeAction
from reactive.ObservableList import ObservableList

on_next = ReactiveTest.on_next
on_error = ReactiveTest.on_error


class RxNotificationTest(unittest.TestCase):
    def setUp(self):
        self.ol = ObservableList([4, 5, 6, 7])
        self.scheduler = TestScheduler()

    def test_ObservableList_append_produces_event(self):
        # arrange
        expected_messages = [on_next(0, 1)]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.append(1)

        # assert
        self.assertEqual(expected_messages, obs.messages)

    def test_ObservableList_append_produces_addEvent(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .subscribe(obs)

        # act
        self.ol.append(2)

        # assert
        self.assertEqual(2, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.ADD, obs.messages[0].value.value.Action)

    def test_ObservableList_remove_produces_remove_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .subscribe(obs)

        # act
        self.ol.remove(4)

        # assert
        self.assertEqual(4, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.REMOVE,
                         obs.messages[0].value.value.Action)

    def test_ObservableList_extend_produces_only_one_event(self):
        # arrange
        expected_messages = [on_next(0, [0, 1, 2, 3])]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.extend([0, 1, 2, 3])

        # assert
        self.assertEqual(expected_messages, obs.messages)
        self.assertEqual(1, len(obs.messages))

    def test_ObservableList_add_multiple_produces_multiple_event(self):
        # arrange
        expected_messages = [on_next(0, 0), on_next(0, 1), on_next(0, 2), on_next(0, 3)]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.append(0)
        self.ol.append(1)
        self.ol.append(2)
        self.ol.append(3)

        # assert
        self.assertEqual(expected_messages, obs.messages)
        self.assertEqual(4, len(obs.messages))

    def test_ObservableList_duplicate_items_produces_events(self):
        # arrange
        expected_messages = [on_next(0, 1), on_next(0, 1), on_next(0, 1)]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.append(1)
        self.ol.append(1)
        self.ol.append(1)

        # assert
        self.assertEqual(expected_messages, obs.messages)

    def test_ObservableList_remove_non_exist_value_produces_on_error(self):
        # arrange
        expected_error = [on_error(0, ValueError('list.remove(x): x not in list'))]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.remove(1)

        # assert
        self.assertEqual(obs.messages, expected_error)

    def test_ObservableList_sort_produces_events_by_default(self):
        # arrange
        expected_messages = [on_next(0, [7, 6, 5, 4])]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.sort(reverse=True)

        # assert
        self.assertEqual(obs.messages, expected_messages)

    def test_ObservableList_sort_can_suppress_event(self):
        # arrange
        expected_messages = []
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.sort(reverse=True, suppress=True)

        # assert
        self.assertEqual(obs.messages, expected_messages)

    def test_ObservableList_reversed_sorts_in_descending_and_not_produce_event(self):
        # arrange
        expected_message = []
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        reverse_list = reversed(self.ol)

        # assert
        self.assertEqual(ObservableList([4, 5, 6, 7]), self.ol)
        self.assertEqual(ObservableList([7, 6, 5, 4]), reverse_list)
        self.assertEqual(obs.messages, expected_message)

    def test_ObservableList_clear_removes_everything_produces_event(self):
        # arrange
        expected_messages = [on_next(0, ())]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.ol.clear()

        # assert
        self.assertEqual(obs.messages, expected_messages)

    def tearDown(self):
        self.ol.dispose()
