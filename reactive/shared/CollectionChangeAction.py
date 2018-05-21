from enum import Enum


class CollectionChangeAction(Enum):
    ADD = 1
    EXTEND = 2
    REMOVE = 3
    REVERSED = 4
    CLEAR = 5
    INDEX = 6
