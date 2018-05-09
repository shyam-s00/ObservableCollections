import unittest

from concurrent.futures import ThreadPoolExecutor
from timeit import timeit

from rx.testing import TestScheduler

from reactive.ObservableList import ObservableList


class ConcurrentModification(unittest.TestCase):

    def setUp(self):
        self.ol = ObservableList([1, 2, 3, 4])
        self.scheduler = TestScheduler()

    def test_try_making_multiple_ops_in_concurrent_futures(self):
        # Not sure if this is testing thread safety of the collection
        # arrange
        obs = self.scheduler.create_observer()
        self.ol.when_collection_changes() \
            .map(lambda x: x.Items) \
            .subscribe(obs)
        # act
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(self.ol.append, 5)
            executor.submit(self.ol.remove, 4)
            executor.submit(self.ol.insert, 7, 0)
            executor.submit(self.ol.extend, [8, 9, 10])
        # assert
        self.assertEqual(4, len(obs.messages))

    def test_observableList_with_stress_append(self):
        # Write similar test cases to stress test the collections performance. 
        setup = '''from reactive.ObservableList import ObservableList
from random import randrange

ol = ObservableList()'''

        cmd = 'ol.append(randrange(0, 2000))'

        result = timeit(cmd, setup=setup, number=20000)
        self.assertIsNotNone(result)
