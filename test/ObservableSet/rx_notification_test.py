import unittest

from rx.testing import TestScheduler, ReactiveTest
from rx.internal import DisposedException

from reactive.shared.CollectionChangeAction import CollectionChangeAction
from reactive.ObservableSet import ObservableSet

on_next = ReactiveTest.on_next
on_error = ReactiveTest.on_error


class RxNotificationObservableSetTest(unittest.TestCase):
    def setUp(self):
        self.os = ObservableSet((4, 5, 6, 7))
        self.scheduler = TestScheduler()

    def test_ObservableSet_add_with_single_item_produces_single_event(self):
        # arrange
        expected_message = [on_next(0, 1)]
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.os.add(1)

        # assert
        self.assertEqual(expected_message, obs.messages)

    def test_ObservableSet_add_with_iterable_produces_single_add_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.add((1, 2, 3))

        # assert
        self.assertEqual(1, len(obs.messages))
        self.assertEqual((1, 2, 3), obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.ADD, obs.messages[0].value.value.Action)

    def test_ObservableSet_update_with_iterable_produces_single_extend_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.update({1, 2, 3, 4})

        # assert
        self.assertEqual(1, len(obs.messages))
        self.assertEqual({1, 2, 3, 4}, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.EXTEND, obs.messages[0].value.value.Action)

    def test_ObservableSet_discard_an_existing_item_produces_remove_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.discard(4)

        # assert
        self.assertEqual(1, len(obs.messages))
        self.assertEqual(4, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.REMOVE, obs.messages[0].value.value.Action)

    def test_ObservableSet_discard_a_non_existing_item_produces_nothing(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_message = []

        self.os.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.os.discard(1)

        # assert
        self.assertEqual(expected_message, obs.messages)

    def test_ObservableSet_remove_an_existing_item_produces_remove_event(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.remove(4)

        # assert
        self.assertEqual(1, len(obs.messages))
        self.assertEqual(4, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.REMOVE, obs.messages[0].value.value.Action)

    def test_ObservableSet_remove_a_non_existing_item_produces_on_error_event(self):
        # arrange
        obs = self.scheduler.create_observer()
        expected_error = [on_error(0, KeyError(1))]

        self.os.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act
        self.os.remove(1)

        # assert
        self.assertEqual(obs.messages, expected_error)

    def test_difference_update_updates_source_and_publish_extend_event(self):
        # arrange
        set_b = ObservableSet((6, 7, 8))
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.difference_update(set_b)

        # assert
        self.assertNotEqual(self.os, ObservableSet((4, 5, 6, 7)))
        self.assertEqual(set_b, ObservableSet((6, 7, 8)))
        self.assertEqual(self.os, ObservableSet((4, 5)))
        self.assertEqual(self.os, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.EXTEND, obs.messages[0].value.value.Action)

    def test_intersection_update_updates_source_and_publish_extend_event(self):
        # arrange
        set_b = ObservableSet((4, 5, 9, 10))
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.intersection_update(set_b)

        # assert
        self.assertNotEqual(self.os, ObservableSet((4, 5, 6, 7)))
        self.assertEqual(set_b, ObservableSet((4, 5, 9, 10)))
        self.assertEqual(self.os, ObservableSet((4, 5)))
        self.assertEqual(self.os, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.EXTEND, obs.messages[0].value.value.Action)

    def test_symmetric_difference_update_updates_sources_and_publish_extend_event(self):
        # arrange
        set_b = ObservableSet((4, 5, 9, 10))
        obs = self.scheduler.create_observer()

        self.os.when_collection_changes() \
            .subscribe(obs)

        # act
        self.os.symmetric_difference_update(set_b)

        # assert
        self.assertNotEqual(self.os, ObservableSet((4, 5, 6, 7)))
        self.assertEqual(set_b, ObservableSet((4, 5, 9, 10)))
        self.assertEqual(self.os, ObservableSet((6, 7, 9, 10)))
        self.assertEqual(self.os, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.EXTEND, obs.messages[0].value.value.Action)

    def test_ObservableSet_with_any_operation_after_dispose_throws_DisposedException(self):
        # arrange
        obs = self.scheduler.create_observer()
        set_b = ObservableSet((4, 5, 9, 10))

        set_b.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)

        # act & assert
        set_b.dispose()
        with self.assertRaises(DisposedException):
            set_b.add(1)

    def tearDown(self):
        self.os.dispose()
