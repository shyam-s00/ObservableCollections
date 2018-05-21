import threading

from abc import ABC, abstractmethod
from collections import Iterable

from rx import Observable, Observer
from rx.core import ObservableBase, Disposable
from rx.internal import DisposedException
from rx.subjects import Subject

from reactive.shared.CollectionChange import CollectionChange


class AbstractObservableCollection(ABC, Iterable):

    def __init__(self):
        self._collectionChanges = Subject()
        self.lock = threading.RLock()
        self.is_disposed = False
        self._suppressNotification = False

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def dispose(self):
        """ Clears all the values from the set, unsubscribe all the subscribers and release resources """
        self.check_disposed()
        self._collectionChanges.dispose()
        self.is_disposed = True

    def when_collection_changes(self) -> ObservableBase:
        return Observable.create(lambda obs: self._subscribe(obs))

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
