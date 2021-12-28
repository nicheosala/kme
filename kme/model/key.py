"""Contains the implementation of a Key object."""
from typing import Any, Final, Optional
from uuid import uuid4, UUID

from jsons import dump, load
from orm.exceptions import NoMatch
from pydantic import BaseModel

from kme import orm
from kme.errors import KeyNotFoundError
from kme.utils import generate_key_material, Instruction, retrieve_key_material


class Key(BaseModel):
    """Random digital data with an associated universally unique ID."""

    key_ID: UUID
    key: str
    key_ID_extension: Optional[Any] = None
    key_extension: Optional[Any] = None

    @staticmethod
    async def get(key_id: UUID, master_sae_id: str) -> 'Key':
        """Get the keys associated to the given SAE ID."""
        try:
            orm_key: Final[orm.Key] = await orm.Key.objects.get(key_id=key_id)
        except NoMatch:
            raise KeyNotFoundError

        instructions: list[Instruction] = load(
            orm_key.instructions,
            list[Instruction],
            strict=True
        )

        # TODO catch errors for block not found.
        key_material: Final[str] = await retrieve_key_material(instructions)

        return Key(
            key_ID=orm_key.key_id,
            key=key_material
        )

    @staticmethod
    async def delete(key_id: UUID) -> None:
        """Delete the key associated to the given key_id."""
        await orm.Key.objects.delete(key_id=key_id)

    @staticmethod
    async def generate(size: int, slave_sae_ids: frozenset[str],
                       *extensions: dict[str, Any]) -> 'Key':
        """Generate one new random key."""
        key_id: Final[UUID] = uuid4()
        key_material, instructions = await generate_key_material(size)

        json_instructions: Final[object] = dump(
            instructions,
            list[Instruction],
            strip_nulls=True,
            strict=True,
            strip_properties=True
        )

        await orm.Key.objects.create(
            key_id=key_id,
            instructions=json_instructions
        )

        return Key(
            key_ID=key_id,
            key=key_material
        )
