"""Fixtures for pytest testing."""
from typing import AsyncIterator

from httpx import AsyncClient
from pytest_asyncio import fixture

from sdn_controller import app


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Return a client stub."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # await local_models.create_all()
        # await shared_models.create_all()
        yield client
        # await local_models.drop_all()
        # await shared_models.drop_all()
