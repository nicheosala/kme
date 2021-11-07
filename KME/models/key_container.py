from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model
from KME.models.error import EmptyValueError
from KME.models.key import Key


@dataclass(frozen=True)
class KeyContainer(Model):
    keys: list[Key]
    key_container_extension: Optional[object] = None

    def __post_init__(self) -> None:
        if self.keys is None:
            raise EmptyValueError
