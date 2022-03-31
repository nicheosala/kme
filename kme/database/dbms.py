"""Manage everything about database."""
import asyncio
import logging
from dataclasses import dataclass
from typing import Final, Any
from uuid import UUID, uuid4

from orm import NoMatch

from kme.configs import Config
from kme.database import orm
from kme.encoder import dump, load
from kme.model import Key as ModelKey
from kme.model.errors import KeyNotFound
from kme.utils import bit_length, collecitonint_to_b64, now


async def clear_routine() -> None:
    while True:
        await asyncio.sleep(Config.TTL // 10)
        await clear()


async def clear() -> None:
    """Delete unnecessary blocks from database.

    A block is deleted if it satisfies at least one of the following conditions:
    - It reached Config.TTL, that is: it is considered too old in order to be used for key generation.
    - Its number of available bits is 0: the block has been completely exploited for key generation.
    """
    await orm.Block.objects.filter(available_bits__exact=0).delete()
    await orm.Block.objects.filter(timestamp__lte=now() - Config.TTL).delete()


lock = asyncio.Lock()


async def get(key_id: UUID, master_sae_id: str | None = None) -> ModelKey:
    """Get the keys associated to the given SAE ID."""
    try:
        orm_key: Final[orm.Key] = await orm.Key.objects.get(key_id=key_id)
    except NoMatch:
        raise KeyNotFound()

    key_material = await retrieve_key_material(orm_key.instructions)

    return ModelKey(orm_key.key_id, key_material)


async def delete(key_id: UUID) -> None:
    """Delete the key associated to the given key_id."""
    await orm.Key.objects.delete(key_id=key_id)


async def generate(
    size: int, slave_sae_ids: frozenset[str] = frozenset(), *extensions: dict[str, Any]
) -> ModelKey:
    """Generate one new random key."""
    key_id: Final[UUID] = uuid4()

    if extensions and (link_id := extensions[0].get("link_id")):
        logging.getLogger("kme").debug(f"Generating key with blocks from link_id {link_id}")
        key_material, json_instructions = await generate_key_material(size, UUID(link_id))
    else:
        logging.getLogger("kme").warning(f"Deprecated: generating key with no link_id specified.")
        key_material, json_instructions = await generate_key_material(size)

    logging.getLogger("kme").debug(
        f"Key {key_id} generated with instructions {json_instructions}"
    )

    await orm.Key.objects.create(key_id=key_id, instructions=json_instructions)

    return ModelKey(key_id, key_material)


async def get_block_by_id(block_id: UUID) -> orm.Block:
    """Get Block with given block_id."""
    try:
        b: orm.Block = await orm.Block.objects.get(block_id=block_id)
        return b
    except NoMatch:
        logging.getLogger("kme").error(f"Block with UUID {block_id} not found.")
        raise KeyNotFound()


@dataclass(frozen=True, slots=True)
class Instruction:
    """An instruction on how to retrieve key material from a block.

    'start' and 'end' works like for function range(): 'start' is included,
    'end' excluded.
    """

    block_id: UUID
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(
                f"Instruction for block {self.block_id} has start "
                f"{self.start} >= end {self.end}"
            )


async def pop_block(link_id: UUID | None) -> orm.Block | None:
    """Retrieve a block from the database, removing it from there.

    This function exploits an async lock, because it has to ensure that the database
    does not return the very same block to multiple requests, before deleting that
    block from the database. The behaviour of pick_block() has to be rimilar to the
    one of list.pop() or Queue.get_nowait()."""
    async with lock:
        b: orm.Block
        if link_id is not None:
            b = (
                await orm.Block.objects.filter(link_id=link_id)
                .filter(available_bits__gt=0)
                .filter(timestamp__gt=now() - Config.TTL)
                .first()
            )
        else:
            b = (
                await orm.Block.objects.filter(available_bits__gt=0)
                .filter(timestamp__gt=now() - Config.TTL)
                .first()
            )

        if b is not None:
            await b.delete()

    return b


async def get_randbits(req_bitlength: int, link_id: UUID | None) -> tuple[list[int], list[Instruction]]:
    """Ask the quantum channel for new blocks.

    If kme does not have a sufficient number of random bits locally, it is forced to
    communicate with the quantum channel, asking for such bits.
    """
    key_material: list[int] = []
    instructions: list[Instruction] = []

    while (diff := req_bitlength - bit_length(key_material)) > 0:
        b = await pop_block(link_id)

        if b is None:
            raise KeyNotFound()

        start = len(b.material) - b.available_bits

        if bit_length(b.material[start:]) > diff:
            end = start + diff // 8
        else:
            end = len(b.material)

        await orm.Block.objects.create(
            block_id=b.block_id,
            link_id=b.link_id,
            material=b.material,
            timestamp=b.timestamp,
            available_bits=len(b.material) - end,
        )

        instructions.append(Instruction(b.block_id, start, end))
        key_material.extend(b.material[start:end])

    return key_material, instructions


async def generate_key_material(req_bitlength: int, link_id: UUID | None = None) -> tuple[str, object]:
    """
    Return key_material encoded as a base64 string, with the 'req_bitlength'
    requested. Alongside the key material, the instructions to re-build it,
    given the exploited blocks, is returned. These instructions have to be
    stored inside the database shared between communicating KMEs.
    """
    assert req_bitlength % 8 == 0

    key_material, instructions = await get_randbits(req_bitlength, link_id)

    return collecitonint_to_b64(key_material), dump(instructions)


async def retrieve_key_material(json_instructions: object) -> str:
    """
    Return the key material re-created based on the given instructions.
    """
    key_material_ints: list[int] = []

    instructions = load(json_instructions, tuple[Instruction, ...])

    for i in instructions:
        b = await get_block_by_id(i.block_id)
        key_material_ints.extend(b.material[i.start : i.end])

    return collecitonint_to_b64(key_material_ints)
