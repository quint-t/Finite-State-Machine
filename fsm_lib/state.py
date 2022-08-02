import collections
from typing import Hashable


class State:
    __slots__ = ('_uid',)

    def __init__(self, uid: Hashable):
        self.uid = uid

    @property
    def uid(self) -> Hashable:
        return self._uid

    @uid.setter
    def uid(self, value: Hashable):
        cls_name = self.__class__.__name__
        if not isinstance(value, Hashable):
            raise TypeError(f'{cls_name}. Argument `value` is not Hashable')
        if isinstance(value, self.__class__):
            raise TypeError(f'`{cls_name}.uid` cannot be an object of class {cls_name}')
        _ = str(value)  # `value` must easily cast to str without throwing an exception
        _ = repr(value)
        self._uid = value

    def copy(self):
        return self.__class__(self.uid)

    def __str__(self) -> str:
        return str(self.uid)

    def __repr__(self) -> str:
        if isinstance(self.uid, tuple):
            return f"{self.__class__.__name__}({tuple(map(repr, self.uid))})"
        return f"{self.__class__.__name__}({repr(self.uid)})"

    def __bool__(self) -> bool:
        return self.uid is not None

    def __eq__(self, other) -> bool:
        try:
            return self.uid == other.uid if isinstance(other, self.__class__) else False
        except:
            return str(self.uid) == str(other.uid)

    def __gt__(self, other) -> bool:
        try:
            return self.uid > other.uid if isinstance(other, self.__class__) else False
        except:
            return str(self.uid) > str(other.uid)

    def __lt__(self, other) -> bool:
        try:
            return self.uid < other.uid if isinstance(other, self.__class__) else False
        except:
            return str(self.uid) < str(other.uid)

    def __ge__(self, other) -> bool:
        try:
            return self.uid >= other.uid if isinstance(other, self.__class__) else False
        except:
            return str(self.uid) >= str(other.uid)

    def __le__(self, other) -> bool:
        try:
            return self.uid <= other.uid if isinstance(other, self.__class__) else False
        except:
            return str(self.uid) <= str(other.uid)

    def __hash__(self) -> int:
        return hash((self.uid,))

    def __contains__(self, item):
        item_uid = item.uid if isinstance(item, State) else item
        q = collections.deque([self])
        while q:
            smth = q.popleft()
            smth_uid = smth.uid if isinstance(smth, State) else smth
            if smth_uid == item_uid:
                return True
            if isinstance(smth, State) and isinstance(smth_uid, (set, frozenset)):
                q.extend(smth_uid)
