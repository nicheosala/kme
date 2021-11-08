from dataclasses import dataclass

from .base_model_ import Model
from .error import EmptyValueError
from .key import Key


@dataclass(frozen=True, slots=True)
class KeyContainer(Model):
    keys: list[Key]
    key_container_extension: object | None = None

    def __post_init__(self) -> None:
        if self.keys is None:
            raise EmptyValueError
