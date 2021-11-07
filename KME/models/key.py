from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model
from KME.models.error import EmptyValueError


@dataclass(frozen=True)
class Key(Model):
    key_ID: str
    key: str
    key_ID_extension: Optional[object] = None
    key_extension: Optional[object] = None

    def __post_init__(self) -> None:
        if self.key_ID is None or self.key is None:
            raise EmptyValueError
