from typing import Final

import pytest
from httpx import AsyncClient

from sd_qkd_node import utils
from sd_qkd_node.database.dbms import generate_key_material


def test_b64_to_iterableint_then_viceversa() -> None:
    s: Final[str] = "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    assert s == utils.collectionint_to_b64(utils.b64_to_tupleint(s))


def test_iterableint_to_b64_then_viceversa() -> None:
    t: Final[tuple[int, ...]] = (8, 13, 255)
    assert t == utils.b64_to_tupleint(utils.collectionint_to_b64(t))


@pytest.mark.asyncio
async def test_generate_key_material(client: AsyncClient, init_blocks: None) -> None:
    req_bitlength: Final[int] = 64
    key_material, _ = await generate_key_material(req_bitlength)
    assert req_bitlength == utils.bit_length_b64(key_material)
