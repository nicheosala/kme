from typing import Iterable
from uuid import UUID

from pytest import fixture

from qcs.orm import Block
from qcs.qc_simulator import QCSimulator
from qcs.resolver import db

example_block: Block = Block(
    time=1640534728,
    ID=UUID('22832407-7a17-4417-a754-71e51b968889'),
    Key=(152, 45, 15, 171, 239, 119, 71, 83, 154, 86, 18, 169, 13, 109, 37,
         238, 128, 163, 129, 126, 193, 222, 2, 48))


# scope='module' if you want to start qcs once in
# the entire test session, instead of starting it once for each test.
@fixture(autouse=True)
def run_qcsimulator() -> Iterable[None]:
    with QCSimulator():
        db.blocks[example_block.ID] = example_block
        yield None
