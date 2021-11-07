from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model
from KME.models.error import EmptyValueError
from KME.models.key_i_ds_key_i_ds import KeyIDsKeyIDs


@dataclass(frozen=True)
class KeyIDs(Model):
    key_IDs: list[KeyIDsKeyIDs]
    key_IDs_extension: Optional[object] = None

    def __post_init__(self) -> None:
        if self.key_IDs is None:
            raise EmptyValueError
