from enum import Enum

class CollectionChangeAction(Enum):
    ADD = 1
    EXTEND = 2
    REMOVE = 3
    REPLACE = 4
    NONE = 5


