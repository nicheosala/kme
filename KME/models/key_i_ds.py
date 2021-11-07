from dataclasses import dataclass

from .base_model_ import Model
from .error import EmptyValueError
from .key_i_ds_key_i_ds import KeyIDsKeyIDs


@dataclass(frozen=True)
class KeyIDs(Model):
    key_IDs: list[KeyIDsKeyIDs]
    key_IDs_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_IDs is None:
            raise EmptyValueError
