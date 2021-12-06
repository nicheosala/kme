from dataclasses import dataclass

from .error import EmptyValueError
from .model import Model


@dataclass(frozen=True, slots=True)
class Key(Model):
    """Random digital data with an associated universally unique ID."""
    key_ID: str
    key: str
    key_ID_extension: object | None = None
    key_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_ID is None or self.key is None:
            raise EmptyValueError
