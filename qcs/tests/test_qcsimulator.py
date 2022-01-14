from typing import Final
from uuid import uuid4

import pytest

from qcs import interface as qci
from qcs.orm import Block
from qcs.resolver import db
from qcs.tests.examples import block_1

pytestmark = pytest.mark.asyncio


async def test_get_blocks() -> None:
    blocks: Final[tuple[Block, ...]] = await qci.gen_blocks()

    assert len(blocks) == 1


async def test_get_multiple_blocks() -> None:
    number: int = 10
    blocks: Final[tuple[Block, ...]] = await qci.gen_blocks(number)

    assert len(blocks) == number


async def test_get_blocks_by_ids() -> None:
    block: Final[Block] = await qci.get_block_by_id(block_1.ID)
    assert block == block_1


async def test_get_blocks_by_ids_with_block_id_not_found() -> None:
    with pytest.raises(qci.BlockNotFound):
        await qci.get_block_by_id(uuid4())


async def test_flush_blocks() -> None:
    await qci.flush_blocks()
    assert len(db.blocks) == 0


async def test_delete_by_ids() -> None:
    await qci.delete_blocks((block_1.ID,))
    with pytest.raises(qci.BlockNotFound):
        await qci.get_block_by_id(block_1.ID)
