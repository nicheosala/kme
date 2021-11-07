from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model


@dataclass(frozen=True)
class EmptyValueError(Exception):

    def __str__(self) -> str:
        return f"Non nullable field set to `None`"


@dataclass(frozen=True)
class Key(Model):
    key_ID: str
    key: str
    key_ID_extension: Optional[object] = None
    key_extension: Optional[object] = None

    def __post_init__(self) -> None:
        if self.key_ID is None or self.key is None:
            raise EmptyValueError

    swagger_types = {
        'key_ID': str,
        'key_ID_extension': object,
        'key': str,
        'key_extension': object
    }

    attribute_map = {
        'key_ID': 'key_ID',
        'key_ID_extension': 'key_ID_extension',
        'key': 'key',
        'key_extension': 'key_extension'
    }
