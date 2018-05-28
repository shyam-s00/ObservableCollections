from reactive.shared.AbstractObservableCollection import AbstractObservableCollection


class ObservableDict(AbstractObservableCollection):

    def __init__(self, items=None):
        self._dict = dict(items) if items is not None else dict()
        super().__init__()

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        pass

    def dispose(self):
        pass
