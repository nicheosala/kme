from typing import Optional, Any

from pydantic import BaseModel

from kme.errors import EmptyValueError
from kme.model import Key


class KeyContainer(BaseModel):
    """
    Key container data format is used for a response data model of API "Get
    key" method and "Get key with key IDs" method.
    """
    keys: tuple[Key, ...]
    key_container_extension: Optional[Any] = None

    def __post_init__(self) -> None:
        if self.keys is None:
            raise EmptyValueError
