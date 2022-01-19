"""This is the only file allowed to communicate with the Quantum Channel."""
from dataclasses import dataclass
from uuid import UUID

from kme.encoder import dump, load
from kme.utils import bit_length, collecitonint_to_b64
from qcs import interface as qci
from qcs.orm import Block as __Block


@dataclass(frozen=True, slots=True)
class Instruction:
    """An instruction on how to retrieve key material from a block."""

    block_id: UUID
    start: int
    end: int


async def generate_key_material(req_bitlength: int) -> tuple[str, object]:
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
        try:
            b: __Block = await qci.gen_block()
        except qci.BlockNotGenerated:
            raise  # TODO

        if bit_length(b.key) >= req_bitlength - bit_length(key_material):
            block_id, start, end = (
                b.id,
                0,
                (req_bitlength - bit_length(key_material)) // 8,
            )
            instructions.append(Instruction(block_id, start, end))
            key_material.extend(b.key[start:end])
            break
        else:
            block_id, start, end = b.id, 0, len(b.key)
            instructions.append(Instruction(block_id, start, end))
            key_material.extend(b.key[start:end])

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
            raise  # TODO

        start, end = instruction.start, instruction.end

        assert end <= len(b.key)

        key_material_ints.extend(b.key[start:end])

    return collecitonint_to_b64(key_material_ints)
