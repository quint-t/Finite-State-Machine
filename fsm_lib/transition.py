from typing import Union, Hashable

from .epsilon import Epsilon


class Transition:
    __slots__ = ('_label',)

    def __init__(self, label: Union[Hashable, None]):
        if label == Epsilon or label is None:
            self.label = str(Epsilon)
        else:
            self.label = label

    @property
    def label(self) -> Hashable:
        return self._label

    @label.setter
    def label(self, value: Hashable):
        cls_name = self.__class__.__name__
        if not isinstance(value, Hashable):
            raise TypeError(f'{cls_name}. Argument `value` is not Hashable')
        if isinstance(value, self.__class__):
            raise TypeError(f'`{cls_name}.label` cannot be an object of class {cls_name}')
        _ = str(value)  # `value` must easily cast to str without throwing an exception
        _ = repr(value)
        self._label = value

    def is_epsilon(self):
        return self.label == Epsilon

    def copy(self):
        return self.__class__(self.label)

    def __str__(self) -> str:
        return str(self.label)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.label)})"

    def __bool__(self) -> bool:
        return self.label is not None

    def __eq__(self, other) -> bool:
        try:
            return self.label == other.label if isinstance(other, self.__class__) else False
        except:
            return str(self.label) == str(other.label)

    def __gt__(self, other) -> bool:
        try:
            return self.label > other.label if isinstance(other, self.__class__) else False
        except:
            return str(self.label) > str(other.label)

    def __lt__(self, other) -> bool:
        try:
            return self.label < other.label if isinstance(other, self.__class__) else False
        except:
            return str(self.label) < str(other.label)

    def __ge__(self, other) -> bool:
        try:
            return self.label >= other.label if isinstance(other, self.__class__) else False
        except:
            return str(self.label) >= str(other.label)

    def __le__(self, other) -> bool:
        try:
            return self.label <= other.label if isinstance(other, self.__class__) else False
        except:
            return str(self.label) <= str(other.label)

    def __hash__(self) -> int:
        return hash((self.label,))
