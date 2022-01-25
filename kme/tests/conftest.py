"""Fixtures for pytest testing."""
from typing import AsyncIterator

from httpx import AsyncClient
from pytest import fixture

from kme import app
from kme.database import orm, models
from kme.tests.examples import key_1, key_2, block_1, block_2


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
    await orm.Block.objects.create(
        block_id=block_1.id, timestamp=block_1.time, material=block_1.key,
        available_bits=len(block_1.key)
    )
    await orm.Block.objects.create(
        block_id=block_2.id, timestamp=block_2.time, material=block_2.key,
        available_bits=len(block_2.key)
    )
