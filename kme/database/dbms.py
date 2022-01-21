"""Manage everything about database."""

from typing import Final, Any
from uuid import UUID, uuid4

from orm import NoMatch

from kme.channel import retrieve_key_material, generate_key_material
from kme.database import orm, database
from kme.model import Key as ModelKey
from kme.model.errors import KeyNotFound


async def get(key_id: UUID, master_sae_id: str) -> ModelKey:
    """Get the keys associated to the given SAE ID."""
    async with database:
        try:
            orm_key: Final[orm.Key] = await orm.Key.objects.get(key_id=key_id)
        except NoMatch:
            raise KeyNotFound

    # TODO catch errors for block not found.
    key_material: Final[str] = await retrieve_key_material(orm_key.instructions)

    return ModelKey(key_ID=orm_key.key_id, key=key_material)


async def delete(key_id: UUID) -> None:
    """Delete the key associated to the given key_id."""
    async with database:
        await orm.Key.objects.delete(key_id=key_id)


async def generate(
    size: int, slave_sae_ids: frozenset[str], *extensions: dict[str, Any]
) -> ModelKey:
    """Generate one new random key."""
    key_id: Final[UUID] = uuid4()
    key_material, json_instructions = await generate_key_material(size)

    async with database:
        await orm.Key.objects.create(key_id=key_id, instructions=json_instructions)

    return ModelKey(key_ID=key_id, key=key_material)
