from typing import AsyncIterator, Final
from uuid import UUID

from httpx import AsyncClient
from pytest import fixture

from kme import app, orm
from kme.database import models

example_key_1: Final[orm.Key] = orm.Key(
    key_id=UUID("bc490419-7d60-487f-adc1-4ddcc177c139"),
    instructions=[{
        'block_id': 'dd6eadfc-23bc-49c0-b9d8-4fb87cb5c18a',
        'start': 0, 'end': 8
    }])

example_key_2: Final[orm.Key] = orm.Key(
    key_id=UUID("0a782fb5-3434-48fe-aa4d-14f41d46cf92"),
    instructions=[{
        'block_id': 'dd6eadfc-23bc-49c0-b9d8-4fb87cb5c18a',
        'start': 0, 'end': 8
    }])


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        await models.create_all()
        yield client
        await models.drop_all()


@fixture
async def init_db() -> None:
    """
    Place inside the database example keys exploited by some tests.
    The tests that want to exploit this fixture must include this fixture name
    as a parameter of the test function.
    """
    await orm.Key.objects.create(
        key_id=example_key_1.key_id,
        instructions=example_key_1.instructions
    )

    await orm.Key.objects.create(
        key_id=example_key_2.key_id,
        instructions=example_key_2.instructions
    )
