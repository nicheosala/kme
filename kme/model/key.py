from dataclasses import dataclass
from typing import Any, Final
from uuid import uuid4, UUID

from kme import orm
from kme.database import session
from kme.errors import EmptyValueError, KeyNotFoundError
from kme.model import Model


@dataclass(frozen=True, slots=True)
class Key(Model):
    """Random digital data with an associated universally unique ID."""
    key_ID: UUID
    key: str
    key_ID_extension: object | None = None
    key_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_ID is None or self.key is None:
            raise EmptyValueError

    @staticmethod
    def get(key_id: UUID, master_sae_id: str) -> 'Key':
        """Get the keys associated to the given SAE ID"""
        key = Key.__fetch(key_id)
        return Key(UUID(key.key_id), key.key_material)

    @staticmethod
    def delete(key_id: UUID) -> None:
        if key := Key.__fetch(key_id):
            session.delete(key)
            session.commit()

    @staticmethod
    def generate(size: int, slave_sae_ids: frozenset[str],
                 *extensions: dict[str, Any]) -> 'Key':
        """Generate one new random key."""
        key_id: Final[UUID] = uuid4()
        key_material: Final[str] = Key.__keygen(size)

        new_key = orm.Key(key_id=str(key_id), key_material=key_material)

        session.add(new_key)
        session.commit()

        return Key(key_id, key_material)

    @staticmethod
    def __keygen(size: int) -> str:
        """Retrieve key material from underlying hardware."""
        return "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
        # TODO this is example key material! You have to ask the quantum
        #  channel for a new key.

    @staticmethod
    def __fetch(key_id: UUID) -> orm.Key:
        key: Final[orm.Key] = session.query(orm.Key) \
            .filter_by(key_id=str(key_id)).one_or_none()
        if key is not None:
            return key

        raise KeyNotFoundError
