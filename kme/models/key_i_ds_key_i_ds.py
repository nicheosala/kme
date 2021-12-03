from dataclasses import dataclass

from .base_model_ import Model
from .error import EmptyValueError


@dataclass(frozen=True, slots=True)
class KeyIDsKeyIDs(Model):
    key_ID: str
    key_ID_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_ID is None:
            raise EmptyValueError