from typing import Iterable

from pytest import fixture

from qcs.resolver import db
from qcs.simulator import Simulator
from qcs.tests.examples import block_1, block_2


@fixture(autouse=True)
# scope='module' if you want to start qcs once in
# the entire test session, instead of starting it once for each test.
def run_qcsimulator() -> Iterable[None]:
    with Simulator():
        db.blocks[block_1.ID] = block_1
        db.blocks[block_2.ID] = block_2
        yield None
        db.blocks.clear()
