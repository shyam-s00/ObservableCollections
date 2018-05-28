from collections import Iterable

from reactive.shared.AbstractObservableCollection import AbstractObservableCollection
from reactive.shared.CollectionChange import CollectionChange


class ObservableList(AbstractObservableCollection):
    
    def __init__(self, items=None):
        self._list = items if items is not None else []
        super().__init__()

    # protocol implementations
    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return ObservableList(list(self._list[index])) if isinstance(index, slice) else self._list[index]

    def __eq__(self, other):
        if not isinstance(other, ObservableList):
            return NotImplemented
        return self._list == other._list

    def __ne__(self, other):
        if not isinstance(other, ObservableList):
            return NotImplemented
        return self._list != other._list

    def __reversed__(self):
        return ObservableList(list(reversed(self._list)))

    def __add__(self, other):
        if not isinstance(other, ObservableList):
            return NotImplemented
        return ObservableList(self._list + other._list)

    def __iter__(self):
        return iter(self._list)

    def __contains__(self, item):
        return item in self._list

    def index(self, item):
        return self._list.index(item)

    # list methods 
    def append(self, item) -> None:
        """ append the object to the end of the list and publishes an event to its subscribers. """
        with self.lock:
            self.check_disposed()
            self._list.append(item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def extend(self, items: Iterable) -> None:
        """ extend the list by appending elements from the iterable and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self._list.extend(items)
            self._onCollectionChanges(CollectionChange.Extend(self, items))

    def insert(self, item, index) -> None:
        """ inserts the object in the specified index and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self._list.insert(index, item)
            self._onCollectionChanges(CollectionChange.Add(self, item))

    def remove(self, item) -> None:
        """ remove first occurrence of the item and publishes the change notification.
        Publishes ValueError to on_error if the item is not present. """
        with self.lock:
            self.check_disposed()
            try:
                self._list.remove(item)
                self._onCollectionChanges(CollectionChange.Remove(self, item))
            except ValueError as ve:
                self._collectionChanges.on_error(ve)
            except Exception as ex:
                self._collectionChanges.on_error(ex)                

    def pop(self) -> None:
        """ remove the last index item from the list and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self._list.pop()
            self._onCollectionChanges(CollectionChange.Remove(self))

    def clear(self) -> None:
        """ remove all the items from the list and publishes the change notification """
        with self.lock:
            self.check_disposed()
            self._list.clear()
            self._onCollectionChanges(CollectionChange.Clear(self))

    def count(self, element) -> int:
        """ return number of occurrences of value """
        with self.lock:
            self.check_disposed()
            return self._list.count(element)

    def sort(self, key=None, reverse=False, suppress=False) -> None:
        """ sort the list in ascending / descending order and publishes the change notification if required. """
        with self.lock:
            self.check_disposed()
            self._list.sort(key=key, reverse=reverse)
            if not suppress:
                self._onCollectionChanges(CollectionChange.IndexChanged(self, self._list))

    def dispose(self):
        """ Clears all the values from the list, unsubscribe all the subscribers and release resources """
        with self.lock:
            self.check_disposed()
            self._beginSuppressNotification()
            self._list.clear()
            self._list = None
            super().dispose()
