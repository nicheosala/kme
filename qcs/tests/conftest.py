from typing import Iterable

from pytest import fixture

from qcs.resolver import db
from qcs.simulator import Simulator
from qcs.tests.examples import block_1, block_2


@fixture(autouse=True)
def run_qcsimulator() -> Iterable[None]:
    with Simulator():
        db.blocks[block_1.ID] = block_1
        db.blocks[block_2.ID] = block_2
        yield None
        db.blocks.clear()
