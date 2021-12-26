from typing import Final

import pytest

from qcs.configs import Test
from qcs.orm import Block
from qcs.qc_interface import QCInterface

qc_interface: Final[QCInterface] = QCInterface(Test())

pytestmark = pytest.mark.asyncio


async def test_get_blocks() -> None:
    blocks: Final[tuple[Block, ...]] = await qc_interface.gen_blocks()

    assert len(blocks) == 1


async def test_get_multiple_blocks() -> None:
    number: int = 10
    blocks: Final[tuple[Block, ...]] = await qc_interface.gen_blocks(
        number)

    assert len(blocks) == number


async def test_get_blocks_by_ids() -> None:
    pass


async def test_flush_blocks() -> None:
    pass


async def test_delete_by_ids() -> None:
    pass
