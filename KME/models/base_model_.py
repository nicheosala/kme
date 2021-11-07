import pprint
import typing
from dataclasses import dataclass

import jsons

T = typing.TypeVar('T')


@dataclass(frozen=True)
class Model(object):
    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        return jsons.load(dikt, cls)

    def to_dict(self) -> object:
        return jsons.dump(self, self.__class__, strip_nulls=True)

    def __repr__(self):
        return pprint.pformat(self.to_dict())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
