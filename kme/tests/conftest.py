from typing import Final, Iterator

from connexion import App
from flask import Flask
from pytest import fixture
from sqlalchemy.orm import Session
from webtest import TestApp

from kme import orm, create_app
from kme.configs import Test
from kme.database import session as _session, engine
from kme.database import mapper_registry


@fixture
def app() -> Iterator[Flask]:
    connexion_app: Final[App] = create_app(Test())
    flask_app: Final[Flask] = connexion_app.app
    with flask_app.test_request_context():
        yield flask_app


@fixture
def test_app(app: Flask) -> TestApp:
    return TestApp(app)


@fixture(autouse=True)
def session() -> Iterator[Session]:
    """A database for the tests."""
    mapper_registry.metadata.create_all(engine)
    setup_initial_data(_session)

    yield _session

    _session.close()
    mapper_registry.metadata.drop_all(engine)


def setup_initial_data(session: Session) -> None:
    k1: Final[orm.Key] = orm.Key(
        key_id="bc490419-7d60-487f-adc1-4ddcc177c139",
        key_material="wHHVxRwDJs3/bXd38GHP3oe4svTuRpZS0yCC7x4Ly+s="
    )

    k2: Final[orm.Key] = orm.Key(
        key_id="0a782fb5-3434-48fe-aa4d-14f41d46cf92",
        key_material="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )

    session.add_all([k1, k2])
    session.commit()
