from typing import Iterator

from fastapi.testclient import TestClient as Client
from pytest import fixture

from kme.tests.testapp import test_app


@fixture
def client() -> Iterator[Client]:
    with Client(test_app) as client:
        yield client
