import threading

from collections import Iterable

from rx import Observable, Observer
from rx.core import ObservableBase, Disposable
from rx.internal import DisposedException
from rx.subjects import Subject

from .CollectionChange import CollectionChange


class ObservableSet:
    def __init__(self, items: Iterable=None):
        self._set = set() if items is None else set(items)
        self.is_disposed = False
        self.lock = threading.RLock()
        self._collectionChanges = Subject()
        self._suppressNotification = False

    # protocol / magic method implementations
    def __len__(self):
        return len(self._set)

    def __contains__(self, item):
        return self._set.__contains__(item)

    # set methods
    def add(self, element):
        with self.lock:
            self.check_disposed()
            self._set.add(element)
            self._onCollectionChanges(CollectionChange.Add(self, element))

    def update(self, items: Iterable) -> None:
        with self.lock:
            self.check_disposed()
            self._set.update(items)
            self._onCollectionChanges(CollectionChange.Extend(self, items))

    def discard(self, element) -> None:
        with self.lock:
            self.check_disposed()
            self._set.discard(element)
            self._onCollectionChanges(CollectionChange.Remove(self, element))

    def remove(self, element) -> None:
        with self.lock:
            self.check_disposed()
            try:
                self._set.remove(element)
                self._onCollectionChanges(CollectionChange.Remove(self, element))
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def pop(self):
        with self.lock:
            self.check_disposed()
            out = self._set.pop()
            self._onCollectionChanges(CollectionChange.Remove(self, out))
            return out

    def clear(self):
        with self.lock:
            self.check_disposed()
            self._set.clear()
            self._onCollectionChanges(CollectionChange.Clear(self))

    # TODO: Move these methods to a base class as its common
    # api methods
    def when_collection_changes(self) -> ObservableBase:
        return Observable.create(lambda obs: self._subscribe(obs))

    def dispose(self):
        """ Clears all the values from the set, unsubscribe all the subscribers and release resources """
        with self.lock:
            self.check_disposed()
            self._beginSuppressNotification()
            self._set.clear()
            self._set = None
            self._collectionChanges.dispose()
            self.is_disposed = True

    def _subscribe(self, observer: Observer) -> Disposable:
        if self.is_disposed:
            return Observable.throw(DisposedException('Trying to access an already disposed object')) \
                    .subscribe(observer)
        else:
            return self._collectionChanges.subscribe(observer)

    def _onCollectionChanges(self, item: CollectionChange):
        if not self._suppressNotification:
            try:
                self._collectionChanges.on_next(item)
            except Exception as ex:
                self._collectionChanges.on_error(ex)

    # internal methods
    def _beginSuppressNotification(self) -> None:
        """ Suppresses all change notification from firing """
        self._suppressNotification = True

    def _endSuppressNotification(self) -> None:
        """ Resumes or Begins pushing change notifications for every subsequent change operations made """
        self._suppressNotification = False

    def check_disposed(self):
        if self.is_disposed:
            raise DisposedException('Trying to access an already disposed object')
