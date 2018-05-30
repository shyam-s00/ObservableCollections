from reactive.shared.AbstractObservableCollection import AbstractObservableCollection
from reactive.shared.CollectionChange import CollectionChange


class ObservableDict(AbstractObservableCollection):

    def __init__(self, items=None):
        self._dict = dict(items) if items is not None else dict()
        super().__init__()

    # protocol / magic method implementation
    def __eq__(self, other):
        if not isinstance(other, ObservableDict):
            return NotImplemented
        return self._dict == other._dict

    def __ne__(self, other):
        if not isinstance(other, ObservableDict):
            return NotImplemented
        return self._dict != other._dict

    def __contains__(self, item):
        return item in self._dict

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)

    def __getitem__(self, key):
        with self.lock:
            return self._dict.__getitem__(key)

    def __delitem__(self, key):
        with self.lock:
            try:
                self._dict.__delitem__(key)
                self._onCollectionChanges(CollectionChange.Remove(self, key))
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def __del__(self):
        with self.lock:
            del self._dict

    # dict methods
    def get(self, key, value=None):
        """ return the value of key. If key does not exists return default value(None) """
        with self.lock:
            self.check_disposed()
            if value is None:
                return self._dict.get(key)
            else:
                return self._dict.get(key, value)

    def items(self):
        """ return a new view of the Observable dictionary's items (key, value) """
        with self.lock:
            self.check_disposed()
            return self._dict.items()

    def keys(self):
        """ return a new view of the Observable dictionary's keys """
        with self.lock:
            self.check_disposed()
            return self._dict.keys()

    def values(self):
        """ return a new view of the Observable dictionary's values """
        with self.lock:
            self.check_disposed()
            return self._dict.values()

    def pop(self, key, value=None):
        """ remove the item with key and return its values or default if the key is not found. Publishes Remove
         event upon successful removal or publishes KeyError to on_error if the key is not found """
        with self.lock:
            self.check_disposed()
            try:
                if value is None:
                    element = self._dict.pop(key)
                else:
                    element = self._dict.pop(key, value)
                self._onCollectionChanges(CollectionChange.Remove(self, element))
                return element
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def popitem(self):
        """ remove and return an arbitrary item(key, value). Publishes Remove event upon successful removal or
        publishes KeyError to on_error if the Observable dictionary is empty """
        with self.lock:
            self.check_disposed()
            try:
                element = self._dict.popitem()
                self._onCollectionChanges(CollectionChange.Remove(self, element))
                return element
            except KeyError as ke:
                self._collectionChanges.on_error(ke)

    def setdefault(self, key, default_value=None):
        """ if the given key is in Observable dictionary, return its values. If not, insert the key with the value
         and return the value (default=None). Only on addition of (key, value) events are published """
        with self.lock:
            self.check_disposed()
            if default_value is None:
                result = self._dict.setdefault(key)
            else:
                result = self._dict.setdefault(key, default_value)

            if default_value == result:
                self._onCollectionChanges(CollectionChange.Add(self, result))

            return result

    def update(self, other=None):
        """ update the dictionary with (key, value) pairs from other Observable dictionary / dictionary, overwriting
         existing keys and publish Extend event """
        with self.lock:
            self.check_disposed()
            if other is not None:
                self._dict.update(other)
                self._onCollectionChanges(CollectionChange.Extend(self, other))

    def clear(self):
        """ removes all items from the Observable dictionary and publishes Clear event"""
        with self.lock:
            self.check_disposed()
            self._dict.clear()
            self._onCollectionChanges(CollectionChange.Clear(self))

    @staticmethod
    def fromkeys(keys, value=None):
        """ return a new Observable dictionary from keys with value for all keys or None """
        if value is None:
            return ObservableDict(dict.fromkeys(keys))
        else:
            return ObservableDict(dict.fromkeys(keys, value))

    def dispose(self):
        """ Clears all the values from the dictionary, unsubscribe all the subscribers and release resources """
        with self.lock:
            self.check_disposed()
            self._beginSuppressNotification()
            self._dict.clear()
            self._dict = None
            super().dispose()
