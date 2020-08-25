import threading

from abc import ABC, abstractmethod
from collections.abc import Iterable

#from rx.core import Observable, Observer, typing

import rx

from rx.core import Observable, Observer
from rx.core.typing import Observable as ObservableBase
from rx.disposable import Disposable
from rx.internal import DisposedException
from rx.subject import Subject
from rx.core.typing import Scheduler
from rx.scheduler import TimeoutScheduler

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

    def when_collection_changes(self) -> rx.core.typing.Observable:
        return rx.create(self._subscribe)

    def _subscribe(self, obs: rx.core.typing.Observer, schd: rx.core.typing.Scheduler) -> rx.core.typing.Disposable:
        if self.is_disposed:
            return rx.throw(DisposedException('Trying to access an already disposed object')).subscribe(observer=obs, scheduler=schd)
        else:
            return self._collectionChanges.subscribe(observer=obs, scheduler=schd)

    def _onCollectionChanges(self, item: CollectionChange):
        if not self._suppressNotification:
            try:
                self._collectionChanges.on_next(item)
            except Exception as ex:
                self._collectionChanges.on_error(error=ex)

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
