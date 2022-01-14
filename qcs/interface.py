from typing import Final
from uuid import UUID

from jsons import dumps

from qcs import client
from qcs.model import Request, GetResponse
from qcs.model.response import DeleteResponse
from qcs.orm import Block


class BlockNotGenerated(Exception):
    """Exception raised when a request of a block generation does not succeed."""


class BlockNotFound(Exception):
    """Exception raised when a request of a block with a given ID does not succeed."""


async def gen_blocks(number: int = 1) -> tuple[Block, ...]:
    """Ask the quantum channel for the generation of n blocks."""
    req: Final[Request] = Request(
        command="Get keys",
        attribute="",
        value=str(number)
    )

    received: Final[str] = await client.send(req)

    res: Final[GetResponse] = GetResponse.from_json(received)

    if len(res.blocks) < number:
        raise BlockNotGenerated

    return res.blocks


async def gen_block() -> Block:
    """Ask the quantum channel for the generation of a single block."""
    blocks = await gen_blocks()
    assert len(blocks) == 1
    return blocks[0]


async def get_block_by_id(block_id: UUID) -> Block:
    """
    Ask the quantum channel for the blocks associated to the given ids.
    """
    blocks = await get_blocks_by_ids((block_id,))
    assert len(blocks) == 1
    return blocks[0]


async def get_blocks_by_ids(block_ids: tuple[UUID, ...]) \
        -> tuple[Block, ...]:
    """
    Ask the quantum channel for the blocks associated to the given ids.
    """
    req: Final[Request] = Request(
        command="Get keys by IDs",
        attribute="",
        value=dumps(block_ids, indent=4)
    )

    received: Final[str] = await client.send(req)

    res: Final[GetResponse] = GetResponse.from_json(received)

    if len(res.blocks) < len(block_ids):
        raise BlockNotFound

    return res.blocks


async def delete_blocks(block_ids: tuple[UUID, ...]) -> DeleteResponse:
    req: Final[Request] = Request(
        command="Delete by IDs",
        attribute="",
        value=dumps(block_ids, indent=4)
    )

    received: Final[str] = await client.send(req)

    res: Final[DeleteResponse] = DeleteResponse.from_json(received)

    return res


async def flush_blocks() -> DeleteResponse:
    req: Final[Request] = Request(
        command="Flush keys",
        attribute="",
        value=""
    )

    received: Final[str] = await client.send(req)

    res: Final[DeleteResponse] = DeleteResponse.from_json(received)
    # TODO This does not respect the specs. The specs does not clarify
    #  what to do in this situation.

    return res
