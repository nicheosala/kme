from typing import AsyncIterator

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pytest import fixture

from kme import app


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
