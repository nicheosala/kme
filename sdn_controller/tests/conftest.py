"""Fixtures for pytest testing."""
from typing import AsyncIterator

from httpx import AsyncClient
from pytest_asyncio import fixture

from sdn_controller import sdn_app
from sdn_controller.database import local_models, shared_models, orm
from sdn_controller.tests.examples import fake_kme


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Return a client stub."""
    async with AsyncClient(app=sdn_app.app, base_url="http://test") as client:
        await local_models.create_all()
        await shared_models.create_all()
        yield client
        await local_models.drop_all()
        await shared_models.drop_all()


@fixture
async def init_kmes() -> None:
    """Add example KMEs into the database."""
    await orm.Kme.objects.create(fake_kme)
