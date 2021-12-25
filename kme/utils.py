from base64 import b64decode, b64encode
from dataclasses import dataclass
from datetime import datetime
from typing import Collection
from uuid import UUID, uuid4


@dataclass
class Instruction:
    block_id: UUID
    start: int
    end: int


def b64_to_tupleint(s: str) -> tuple[int, ...]:
    """Convert a base64-encoded string into a tuple of integer numbers in
    range [0, 255]. """
    return tuple(b for b in b64decode(s))


def collecitonint_to_b64(c: Collection[int]) -> str:
    """Convert a collection of integer numbers in range [0, 255] into a
    base64-encoded string. """
    assert all(n in range(0, 256) for n in c)
    return str(b64encode(bytes(c)), 'utf-8')


def bit_length(c: Collection[int]) -> int:
    """
    Return the number of bits represented by the given collection of integer
    numbers in range [0, 255]. Each positive integer number is considered
    8-bits long.
    """
    assert all(n in range(0, 256) for n in c)
    return len(c) * 8


def bit_length_b64(s: str) -> int:
    """Return the number of bits represented by the given base64 string."""
    return bit_length((b64_to_tupleint(s)))


async def generate_key_material(req_bitlength: int) \
        -> tuple[str, list[Instruction]]:
    """
    Return key_material encoded as a base64 string, with the 'req_bitlength'
    requested. Alongside the key material, the instructions to re-build it,
    given the exploited blocks, is returned. These instructions have to be
    stored inside the database shared between communicating KMEs.
    """
    assert req_bitlength % 8 == 0
    key_material: list[int] = []
    instructions: list[Instruction] = []

    while True:
        b: Block = await generate_block()
        if bit_length(b.Key) >= req_bitlength - bit_length(key_material):
            block_id, start, end = b.ID, 0, (
                    req_bitlength - bit_length(key_material)) // 8
            instructions.append(Instruction(block_id, start, end))
            key_material.extend(b.Key[start:end])
            break
        else:
            block_id, start, end = b.ID, 0, len(b.Key)
            instructions.append(Instruction(block_id, start, end))
            key_material.extend(b.Key[start:end])

    return collecitonint_to_b64(key_material), instructions


async def retrieve_key_material(instructions: list[Instruction]) -> str:
    """
    Return the key material re-created based on the given instructions.
    """
    key_material_ints: list[int] = []

    for instruction in instructions:
        block: Block = await get_block_by_id(instruction.block_id)
        start, end = instruction.start, instruction.end

        assert end <= len(block.Key)

        key_material_ints.extend(block.Key[start:end])

    return collecitonint_to_b64(key_material_ints)


# TODO Follows code to be removed #####


@dataclass
class Block:
    time: int
    ID: UUID
    Key: tuple[int, ...]


class BlockNotFound(Exception):
    pass


async def generate_block() -> Block:
    # TODO This has to be retrieved from quantum channel.
    return Block(_timestamp(), uuid4(), _get_random_bits())


async def get_block_by_id(block_id: UUID) -> Block:
    # TODO This has to be retrieved from quantum channel.
    return Block(_timestamp(), uuid4(), _get_random_bits())


def _timestamp() -> int:
    return int(datetime.now().timestamp())


def _get_random_bits() -> tuple[int, ...]:
    from random import getrandbits, randint
    return tuple(getrandbits(8) for _ in range(randint(10, 50)))
