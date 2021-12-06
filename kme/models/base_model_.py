from dataclasses import dataclass

from jsons import JsonSerializable, dumps


@dataclass(frozen=True, slots=True)
class Model(JsonSerializable):

    def to_json(self) -> object:
        return self.dump(strip_nulls=True)

    def __repr__(self) -> str:
        return dumps(self.to_json())

    def __str__(self) -> str:
        return dumps(self.to_json())

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
