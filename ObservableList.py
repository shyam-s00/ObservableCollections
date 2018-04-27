import threading
import time

from rx import Observable, Observer
from rx.core import ObservableBase
from rx.disposables import AnonymousDisposable
from rx.subjects import Subject
from rx.internal import DisposedException

from collections import Iterable
from collections.abc import Sequence
from CollectionChangeAction import CollectionChangeAction
from CollectionChange import CollectionChange

class ObservableList(Sequence):
    
    def __init__(self, items = None):
        self.list = items if items is not None else []
        self._collectionChanges = Subject()
        self.lock = threading.RLock() 
        self.is_disposed = False

    # protocol implementations
    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __eq__(self, rhs):
        if not isinstance(rhs, ObservableList):
            return NotImplemented
        return self.list == rhs.list

    # list methods 
    def append(self, item) -> None:
        with self.lock:
            self.check_disposed()
            self.list.append(item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def extend(self, items: Iterable) -> None:
        with self.lock:
            self.check_disposed()
            self.list.extend(items)
            self._onCollectionChanges(CollectionChange.Extend(self, items))

    def insert(self, item, index) -> None:
        with self.lock:
            self.check_disposed()
            self.list.insert(index, item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def remove(self, item) -> None:
        with self.lock:
            self.check_disposed()
            self.list.remove(item)
            self._onCollectionChanges(CollectionChange.Remove(self, item))

    def pop(self) -> None:
        with self.lock:
            self.check_disposed()
            self.list.pop()
            self._onCollectionChanges(CollectionChange.Remove(self))

    # public API method
    def when_collection_changes(self) -> ObservableBase:
        return Observable.create(lambda obs: self._subscribe(obs))

    def dispose(self):
        with self.lock:            
            self.list.clear()
            self.list = None
            self._collectionChanges.dispose()
            self.is_disposed = True

    # internal methods 
    def check_disposed(self):
        if self.is_disposed:
            raise DisposedException('Trying to access an already disposed object')

    def _subscribe(self, observer: Observer) -> AnonymousDisposable:
        if self.is_disposed:
            return Observable.throw(DisposedException('Trying to access an already disposed object')) \
                    .subscribe(observer)
        else:
            return self._collectionChanges.subscribe(observer)

    def _onCollectionChanges(self, item: CollectionChange):
        try:
            self._collectionChanges.on_next(item)
        except Exception as ex:
            self._collectionChanges.on_error(ex)
