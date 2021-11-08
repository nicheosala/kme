from dataclasses import dataclass
from pprint import pformat
from typing import TypeVar

from jsons import load, dump

T = TypeVar('T')


@dataclass(frozen=True, slots=True)
class Model(object):
    @classmethod
    def from_dict(cls: T, dikt) -> T:
        return load(dikt, cls)

    def to_dict(self) -> object:
        return dump(self, self.__class__, strip_nulls=True)

    def __repr__(self):
        return pformat(self.to_dict())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
