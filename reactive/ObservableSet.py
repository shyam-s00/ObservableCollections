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
        """ Add an element to an ObservableSet. Publishes change notification """
        with self.lock:
            self.check_disposed()
            self._set.add(element)
            self._onCollectionChanges(CollectionChange.Add(self, element))

    def update(self, items: Iterable) -> None:
        """ Update an ObservableSet with the union of itself and others. Publishes change notification """
        with self.lock:
            self.check_disposed()
            self._set.update(items)
            self._onCollectionChanges(CollectionChange.Extend(self, items))

    def discard(self, element) -> None:
        """ Remove an element from a set if it is a member. Publishes change notification if an item is removed
        If the element is not a member, do nothing. """
        with self.lock:
            self.check_disposed()
            if element in self._set:
                self._set.discard(element)
                self._onCollectionChanges(CollectionChange.Remove(self, element))

    def remove(self, element) -> None:
        """ Remove an element from n ObservableSet; it must be a member. Publishes change notifications
        If the element is not a member, publishes KeyError to on_error channel. """
        with self.lock:
            self.check_disposed()
            try:
                self._set.remove(element)
                self._onCollectionChanges(CollectionChange.Remove(self, element))
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def pop(self):
        """ Remove and return an arbitrary ObservableSet element. Publishes change notifications
        Publishes KeyError to on_error channel if the set is empty."""
        with self.lock:
            self.check_disposed()
            try:
                out = self._set.pop()
                self._onCollectionChanges(CollectionChange.Remove(self, out))
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def clear(self):
        """ Remove all elements from this ObservableSet. Publishes change notifications """
        with self.lock:
            self.check_disposed()
            self._set.clear()
            self._onCollectionChanges(CollectionChange.Clear(self))

    def difference_update(self, *args: Iterable) -> None:
        """ Remove all elements of another ObservableSet from this ObservableSet. Publishes change notifications """
        with self.lock:
            self.check_disposed()
            self._set.difference_update(args)
            self._onCollectionChanges(CollectionChange.Extend(self, self._set))  # Need better name...

    def intersection_update(self, *args: Iterable) -> None:
        """ Update an ObservableSet with the intersection of itself and another. Publishes change notifications """
        with self.lock:
            self.check_disposed()
            self._set.intersection_update(args)
            self._onCollectionChanges(CollectionChange.Extend(self, self._set))

    def symmetric_difference_update(self, *args: Iterable) -> None:
        """ Update an ObservableSet with the symmetric difference of itself and another.
        Publishes change notification """
        with self.lock:
            self.check_disposed()
            self._set.symmetric_difference_update(args)
            self._onCollectionChanges(CollectionChange.Extend(self, self._set))

    def difference(self, *args):
        """ Return the difference of two or more ObservableSets as a new ObservableSet.
        *Does not publish change notifications* """
        with self.lock:
            self.check_disposed()
            return ObservableSet(self._set.difference(args))

    def intersection(self, *args: Iterable):
        """ Return the intersection of two ObservableSets as a new ObservableSet.
        *Does not publish change notifications* """
        with self.lock:
            self.check_disposed()
            return ObservableSet(self._set.intersection(args))

    def symmetric_difference(self, *args: Iterable):
        """ Return the symmetric difference of two ObservableSets as a new ObservableSet.
        *Does not publish change notifications* """
        with self.lock:
            self.check_disposed()
            return ObservableSet(self._set.symmetric_difference(args))

    def union(self, *args):
        """ Return the union of ObservableSets as a new ObservableSet. *Does not publish change notification* """
        with self.lock:
            self.check_disposed()
            return ObservableSet(self._set.union(args))

    def isdisjoint(self, *args: Iterable) -> bool:
        """ Return True if two ObservableSets have a null intersection. *Does not publish change notification* """
        with self.lock:
            self.check_disposed()
            return self._set.isdisjoint(args)

    def issubset(self, *args: Iterable) -> bool:
        """ Report whether another ObservableSet contains this ObservableSet.
        *Does not publish change notifications* """
        with self.lock:
            self.check_disposed()
            return self._set.issubset(args)

    def issuperset(self, *args: Iterable) -> bool:
        """ Report whether this ObservableSet contains another ObservableSet.
        *Does not publish change notifications* """
        with self.lock:
            self.check_disposed()
            return self._set.issuperset(args)

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
