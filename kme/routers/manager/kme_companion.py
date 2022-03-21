"""
This file contains an interface that the two KMEs involved in a communication can
exploit. It is mandatory not to directly communicate secrets (e.g.: key material)
over this interface.
"""
from typing import Final
from uuid import UUID

from fastapi import APIRouter, Query

from kme.database.dbms import generate
from kme.model.key_container import Key

router: Final[APIRouter] = APIRouter(tags=["companion"])


@router.get("/gen_keys", include_in_schema=False)
async def gen_keys(
    number: int = Query(default=1, description="Number of keys requested", ge=1),
    size: int = Query(default=64, description="Size of each key in bits", ge=1),
) -> tuple[UUID, ...]:
    """Return UUIDs associated to newly generated keys."""
    new_keys: Final[list[UUID]] = []
    for _ in range(number):
        new_key: Key = await generate(size)
        new_keys.append(new_key.key_ID)

    return tuple(new_keys)
