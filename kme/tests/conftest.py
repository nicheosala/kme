"""Fixtures for pytest testing."""
from typing import AsyncIterator, Iterable

from httpx import AsyncClient
from pytest import fixture

from kme import app
from kme.database import orm, models
from kme.tests.examples import key_1, key_2


@fixture(autouse=True)
def run_qcsimulator() -> Iterable[None]:
    """Start a Quantum Channel simulator."""
    from qcs import Simulator
    from qcs.resolver import db
    from qcs.tests.examples import block_1, block_2

    with Simulator():
        db.blocks[block_1.id] = block_1
        db.blocks[block_2.id] = block_2
        yield None
        db.blocks.clear()


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Return a client stub."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        await models.create_all()
        yield client
        await models.drop_all()


@fixture()
async def init_db() -> None:
    """Initialize the database.

    Place inside the database example keys exploited by some tests.
    The tests that want to exploit this fixture must include this fixture name
    as a parameter of the test function.
    """
    await orm.Key.objects.create(key_id=key_1.key_id, instructions=key_1.instructions)

    await orm.Key.objects.create(key_id=key_2.key_id, instructions=key_2.instructions)
