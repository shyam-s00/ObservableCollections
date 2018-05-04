from collections import Iterable

from .CollectionChangeAction import CollectionChangeAction

class CollectionChange:
    """ A class method that holds the collection change type, source and changed items. Also provides factory methods for creating  
        type of collection change events """
    def __init__(self, source = None, action = None, items = None):
        self.source = source if source is not None else []  # consider changing this into tuple as it need not be mutable.
        self.action: CollectionChangeAction = action
        self.items = items if items is not None else [] # consider changing this into tuple as it need not be mutable.

    @property
    def Source(self):
        return self.source

    @property
    def Items(self):
        return self.items

    @property
    def Action(self):
        return self.action

    @classmethod
    def Add(cls, source, items):
        return cls(source=source, action=CollectionChangeAction.ADD, items=items)

    @classmethod
    def Remove(cls, source, items=None):
        return cls(source=source, action=CollectionChangeAction.REMOVE, items=items)

    @classmethod
    def Extend(cls, source, items: Iterable):
        return cls(source=source, action=CollectionChangeAction.EXTEND, items=items)

    @classmethod
    def Clear(cls, source):
        return cls(source=source, action=CollectionChangeAction.CLEAR)

    @classmethod
    def IndexChanged(cls, source):
        return cls(source=source, action=CollectionChangeAction.INDEX, items=source.list)
