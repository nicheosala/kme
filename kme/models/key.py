from dataclasses import dataclass
from typing import Any, Final
from uuid import uuid4

from immutabledict import immutabledict

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

    @staticmethod
    def get(key_id: str, master_sae_id: str) -> 'Key':
        """Get the keys associated to the given SAE ID"""
        # TODO Get key from database
        return Key("3fa85f64-5717-4562-b3fc-2c963f66afa6", "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA=")

    @staticmethod
    def remove(key_id: str) -> None:
        # TODO delete key from database
        pass

    @staticmethod
    def generate(size: int, slave_sae_ids: frozenset[str], *params: immutabledict[str, Any]) -> 'Key':
        """Generate one new random key."""
        key_id: Final[str] = str(uuid4())
        new_key: Final[str] = Key.__keygen(size)
        # TODO Add key to database
        return Key(key_id, new_key)

    @staticmethod
    def __keygen(size: int) -> str:
        """Retrieve key material from underlying hardware."""
        return "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
        # TODO this is example key material! You have to ask the quantum channel for a new key.
