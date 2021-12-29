from typing import Final

import pytest

from kme import utils
from kme.channel.qc import generate_key_material

pytestmark = pytest.mark.asyncio


def test_b64_to_iterableint_then_viceversa() -> None:
    s: Final[str] = "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    assert s == utils.collecitonint_to_b64(utils.b64_to_tupleint(s))


def test_iterableint_to_b64_then_viceversa() -> None:
    t: Final[tuple[int, ...]] = (8, 13, 255)
    assert t == utils.b64_to_tupleint(utils.collecitonint_to_b64(t))


async def test_generate_key_material() -> None:
    req_bitlength: Final[int] = 256
    key_material, _ = await generate_key_material(req_bitlength)
    assert req_bitlength == utils.bit_length_b64(key_material)
