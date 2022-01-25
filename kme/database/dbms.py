"""Manage everything about database."""
import logging
from dataclasses import dataclass
from typing import Final, Any
from uuid import UUID, uuid4

from orm import NoMatch

from kme.database import database, orm
from kme.database.orm import Block
from kme.encoder import dump, load
from kme.model import Key as ModelKey
from kme.model.errors import KeyNotFound
from kme.utils import bit_length, collecitonint_to_b64


async def get(key_id: UUID, master_sae_id: str) -> ModelKey:
    """Get the keys associated to the given SAE ID."""
    async with database:
        try:
            orm_key: Final[orm.Key] = await orm.Key.objects.get(key_id=key_id)
        except NoMatch:
            raise KeyNotFound()

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

    logging.getLogger("kme").debug(
        f"Key {key_id} generated with instructions {json_instructions}"
    )

    async with database:
        await orm.Key.objects.create(key_id=key_id, instructions=json_instructions)

    return ModelKey(key_ID=key_id, key=key_material)


async def pick_block() -> Block:
    """Pick a Block from the database.

    Get a block with available bits and remove it from the database."""
    async with database:
        b: Block = await Block.objects.filter(available_bits__gt=0).first()

    if b is None:
        raise KeyNotFound()

    async with database:
        await b.delete()

    return b


async def get_block_by_id(block_id: UUID) -> Block:
    """Get Block with given block_id."""
    async with database:
        try:
            b: Block = await orm.Block.objects.get(block_id=block_id)
            return b
        except NoMatch:
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


async def get_randbits(req_bitlength: int) -> tuple[list[int], list[Instruction]]:
    """Ask the quantum channel for new blocks.

    If kme does not have a sufficient number of random bits locally, it is forced to
    communicate with the quantum channel, asking for such bits.
    """
    key_material: list[int] = []
    instructions: list[Instruction] = []

    while (diff := req_bitlength - bit_length(key_material)) > 0:
        b = await pick_block()
        start = len(b.material) - b.available_bits

        if bit_length(b.material[start:]) > diff:
            end = start + diff // 8
        else:
            end = len(b.material)

        async with database:
            print(await orm.Block.objects.get(block_id=b.block_id))

        # async with database:
        #     await orm.Block.objects.create(
        #         block_id=b.block_id,
        #         material=b.material,
        #         timestamp=b.timestamp,
        #         available_bits=len(b.material) - end,
        #     )

        instructions.append(Instruction(b.block_id, start, end))
        key_material.extend(b.material[start:end])

    return key_material, instructions


async def generate_key_material(req_bitlength: int) -> tuple[str, object]:
    """
    Return key_material encoded as a base64 string, with the 'req_bitlength'
    requested. Alongside the key material, the instructions to re-build it,
    given the exploited blocks, is returned. These instructions have to be
    stored inside the database shared between communicating KMEs.
    """
    assert req_bitlength % 8 == 0

    key_material, instructions = await get_randbits(req_bitlength)

    return collecitonint_to_b64(key_material), dump(instructions)


async def retrieve_key_material(json_instructions: object) -> str:
    """
    Return the key material re-created based on the given instructions.
    """
    key_material_ints: list[int] = []

    instructions: tuple[Instruction, ...] = load(
        json_instructions, tuple[Instruction, ...]
    )

    for i in instructions:
        b = await get_block_by_id(i.block_id)
        key_material_ints.extend(b.material[i.start: i.end])

    return collecitonint_to_b64(key_material_ints)
