from typing import Final

from connexion import App
from pytest import fixture
from webtest import TestApp

from ..__main__ import create_app
from ..configs import Test


@fixture
def app() -> App:
    _app: Final[App] = create_app(Test())
    context = _app.app.test_request_context()
    context.push()

    yield _app.app

    context.pop()


@fixture
def test_app(app: App) -> TestApp:
    return TestApp(app)
