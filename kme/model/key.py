from typing import Any, Final, Optional
from uuid import uuid4, UUID

from orm.exceptions import NoMatch
from pydantic import BaseModel

from kme import orm
from kme.errors import KeyNotFoundError


class Key(BaseModel):
    """Random digital data with an associated universally unique ID."""
    key_ID: UUID
    key: str
    key_ID_extension: Optional[Any] = None
    key_extension: Optional[Any] = None

    @staticmethod
    async def get(key_id: UUID, master_sae_id: str) -> 'Key':
        """Get the keys associated to the given SAE ID"""
        try:
            key: Final[orm.Key] = await orm.Key.objects.get(key_id=key_id)
            return Key(
                key_ID=key.key_id,
                key=key.key_material
            )
        except NoMatch:
            raise KeyNotFoundError

    @staticmethod
    async def delete(key_id: UUID) -> None:
        await orm.Key.objects.delete(key_id=key_id)

    @staticmethod
    async def generate(size: int, slave_sae_ids: frozenset[str],
                       *extensions: dict[str, Any]) -> 'Key':
        """Generate one new random key."""
        key_id: Final[UUID] = uuid4()
        key_material: Final[str] = Key.__keygen(size)

        await orm.Key.objects.create(
            key_id=key_id,
            key_material=key_material
        )

        return Key(
            key_ID=key_id,
            key=key_material
        )

    @staticmethod
    def __keygen(size: int) -> str:
        """Retrieve key material from underlying hardware."""
        return "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
        # TODO this is example key material! You have to ask the quantum
        #  channel for a new key.
