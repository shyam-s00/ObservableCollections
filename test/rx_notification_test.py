import unittest

from rx.testing import ReactiveTest, TestScheduler

from ObservableList import ObservableList
from CollectionChange import CollectionChange
from CollectionChangeAction import CollectionChangeAction

on_next = ReactiveTest.on_next

class RxNotificationTest(unittest.TestCase):
    def setUp(self):
        self.ol = ObservableList([4,5,6,7])
        self.scheduler = TestScheduler()

    def test_Observablelist_append_produces_event(self):
        # arrange
        expectedMessages = [ on_next(0, 1) ]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
                .map(lambda x: x.Items) \
                .subscribe(obs)
        
        # act
        self.ol.append(1)
        
        # assert
        self.assertEqual(expectedMessages, obs.messages)

    def test_observablelist_append_produces_addEvent(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
                    .subscribe(obs)

        # act
        self.ol.append(2)
        
        # assert
        self.assertEqual(2, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.ADD, obs.messages[0].value.value.Action)

    def test_observablelist_remove_produces_removeEvent(self):
        # arrange
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
                    .subscribe(obs)

        # act
        self.ol.remove(4)
        
        # assert
        self.assertEqual(4, obs.messages[0].value.value.Items)
        self.assertEqual(CollectionChangeAction.REMOVE, obs.messages[0].value.value.Action)


    def test_observablelist_extend_produces_onlyone_event(self):
        # arrange
        expectedMessages = [on_next(0, [0,1,2,3])]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
                    .map(lambda x: x.Items) \
                    .subscribe(obs)

        # act
        self.ol.extend([0,1,2,3])

        # assert
        self.assertEqual(expectedMessages, obs.messages)
        self.assertEqual(1, len(obs.messages))


    def test_observablelist_add_multiple_produces_multiple_event(self):
        # arrange
        expectedMessages = [on_next(0, 0), on_next(0, 1), on_next(0, 2), on_next(0, 3)]
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
        self.assertEqual(expectedMessages, obs.messages)
        self.assertEqual(4, len(obs.messages))

    def test_Observablelist_duplicate_items_produces_events(self):
        # arrange
        expectedMessages = [ on_next(0, 1), on_next(0, 1), on_next(0, 1) ]
        obs = self.scheduler.create_observer()

        self.ol.when_collection_changes() \
                .map(lambda x: x.Items) \
                .subscribe(obs)
        
        # act
        self.ol.append(1)
        self.ol.append(1)
        self.ol.append(1)
        
        # assert
        self.assertEqual(expectedMessages, obs.messages)
