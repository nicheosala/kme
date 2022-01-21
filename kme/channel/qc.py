"""This is the only file allowed to communicate with the Quantum Channel."""
from dataclasses import dataclass
from uuid import UUID

from kme.encoder import dump, load
from kme.model.errors import KeyNotFound
from kme.utils import bit_length, collecitonint_to_b64
from qcs import interface as qci
from qcs.orm import Block as __Block


@dataclass(frozen=True, slots=True)
class Instruction:
    """An instruction on how to retrieve key material from a block.

    'start' and 'end' works like for function range(): 'start' is included,
    'end' excluded.
    """

    block_id: UUID
    start: int
    end: int


async def get_randbits_from_local_storage(
    req_bitlength: int, key_material: list[int], instructions: list[Instruction]
) -> tuple[list[int], list[Instruction]]:
    """Ask the local storage for random bits."""
    return key_material, instructions  # TODO exploit locally stored random bits.


async def get_randbits_from_quantum_channel(
    req_bitlength: int, key_material: list[int], instructions: list[Instruction]
) -> tuple[list[int], list[Instruction]]:
    """Ask the quantum channel for new blocks.

    If kme does not have a sufficient number of random bits locally, it is forced to
    communicate with the quantum channel, asking for such bits.
    """
    while (diff := req_bitlength - bit_length(key_material)) > 0:
        try:
            b: __Block = await qci.gen_block()
        except qci.BlockNotGenerated:
            raise KeyNotFound()

        end = diff // 8 if bit_length(b.key) >= diff else len(b.key)

        instructions.append(Instruction(b.id, 0, end))
        key_material.extend(b.key[:end])

    # TODO store remaining unusued block locally.

    return key_material, instructions


async def generate_key_material(req_bitlength: int) -> tuple[str, object]:
    """
    Return key_material encoded as a base64 string, with the 'req_bitlength'
    requested. Alongside the key material, the instructions to re-build it,
    given the exploited blocks, is returned. These instructions have to be
    stored inside the database shared between communicating KMEs.
    """
    assert req_bitlength % 8 == 0

    key_material, instructions = await get_randbits_from_local_storage(
        req_bitlength, [], []
    )

    key_material, instructions = await get_randbits_from_quantum_channel(
        req_bitlength, key_material, instructions
    )

    return collecitonint_to_b64(key_material), dump(instructions)


async def retrieve_key_material(json_instructions: object) -> str:
    """
    Return the key material re-created based on the given instructions.
    """
    key_material_ints: list[int] = []

    instructions: tuple[Instruction, ...] = load(
        json_instructions, tuple[Instruction, ...]
    )

    for instruction in instructions:
        try:
            b: __Block = await qci.get_block_by_id(instruction.block_id)
        except qci.BlockNotFound:
            raise KeyNotFound()

        start, end = instruction.start, instruction.end

        assert end <= len(b.key)

        key_material_ints.extend(b.key[start:end])

    return collecitonint_to_b64(key_material_ints)
