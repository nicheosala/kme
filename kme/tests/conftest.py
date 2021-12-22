from typing import Iterator

from fastapi.testclient import TestClient as Client
from pytest import fixture

from kme import app


@fixture
def client() -> Iterator[Client]:
    with Client(app) as client:
        yield client
