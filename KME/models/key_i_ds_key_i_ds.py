from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model
from KME.models.error import EmptyValueError


@dataclass(frozen=True)
class KeyIDsKeyIDs(Model):
    key_ID: str
    key_ID_extension: Optional[object]

    def __post_init__(self) -> None:
        if self.key_ID is None:
            raise EmptyValueError
