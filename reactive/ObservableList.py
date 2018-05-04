import threading
import time

from rx import Observable, Observer
from rx.core import ObservableBase
from rx.disposables import AnonymousDisposable
from rx.subjects import Subject
from rx.internal import DisposedException

from collections import Iterable
from collections.abc import Sequence

from .CollectionChangeAction import CollectionChangeAction
from .CollectionChange import CollectionChange

class ObservableList(Sequence):
    
    def __init__(self, items = None):
        self.list = items if items is not None else []
        self._collectionChanges = Subject()
        self.lock = threading.RLock() 
        self.is_disposed = False
        self._supressNotification = False

    # protocol implementations
    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __eq__(self, rhs):
        if not isinstance(rhs, ObservableList):
            return NotImplemented
        return self.list == rhs.list

    def __reversed__(self):
        return reversed(self.list)

    # list methods 
    def append(self, item) -> None:
        """ append the object to the end of the list and publishes an event to its subscribers. """
        with self.lock:
            self.check_disposed()
            self.list.append(item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def extend(self, items: Iterable) -> None:
        """ extend the list by appending elements from the iterable and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self.list.extend(items)
            self._onCollectionChanges(CollectionChange.Extend(self, items))

    def insert(self, item, index) -> None:
        """ inserts the object in the specified index and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self.list.insert(index, item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def remove(self, item) -> None:
        """ remove first occurence of the item and publishes the change notification. Publishes ValueError to on_error if the item is not present. """
        with self.lock:
            self.check_disposed()
            try:
                self.list.remove(item)
                self._onCollectionChanges(CollectionChange.Remove(self, item))
            except ValueError as ve:
                self._collectionChanges.on_error(ve)
            except Exception as ex:
                self._collectionChanges.on_error(ex)                

    def pop(self) -> None:
        """ remove the last index item from the list and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self.list.pop()
            self._onCollectionChanges(CollectionChange.Remove(self))

    def clear(self) -> None:
        """ remove all the items from the list and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self.list.clear()
            self._onCollectionChanges(CollectionChange.Clear(self))

    def count(self, element) -> int:
        """ return number of occurrences of value """
        with self.lock:
            self.check_disposed()
            return self.list.count(element)

    def sort(self, key=None, reverse=False, suppress=False) -> None:
        """ sort the list in ascending / descending order and publishes the change notification if required. """
        with self.lock:
            self.check_disposed()
            self.list.sort(key=key, reverse=reverse)
            if not suppress:
                self._onCollectionChanges(CollectionChange.IndexChanged(self))

    # public API method
    def when_collection_changes(self) -> ObservableBase:
        return Observable.create(lambda obs: self._subscribe(obs))

    def dispose(self):
        """ Clears all the value from the list, unsubcribes all the subscribers and release resources """
        with self.lock:
            self._beginSuppressNotification()
            self.list.clear()
            self.list = None
            self._collectionChanges.dispose()
            self.is_disposed = True

    # internal methods 
    def check_disposed(self):
        if self.is_disposed:
            raise DisposedException('Trying to access an already disposed object')

    def _beginSuppressNotification(self) -> None:
        """ Suppresses all change notification from firing """
        self._supressNotification = True

    def _endSuppressNotification(self) -> None:
        """ Resumes or Begins pushing change notificaions for every subsequent change operations made """
        self._supressNotification = False

    def _subscribe(self, observer: Observer) -> AnonymousDisposable:
        if self.is_disposed:
            return Observable.throw(DisposedException('Trying to access an already disposed object')) \
                    .subscribe(observer)
        else:
            return self._collectionChanges.subscribe(observer)

    def _onCollectionChanges(self, item: CollectionChange):
        if not self._supressNotification:
            try:
                self._collectionChanges.on_next(item)
            except Exception as ex:
                self._collectionChanges.on_error(ex)
