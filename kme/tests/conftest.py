from typing import Final, Iterator

from connexion import App
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest import fixture
from webtest import TestApp

from kme import orm, create_app
from kme.configs import Test
from kme.database import db as _db


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
def db(app: Flask) -> Iterator[SQLAlchemy]:
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    setup_initial_data(_db)

    yield _db

    _db.session.close()
    _db.drop_all()


def setup_initial_data(db: SQLAlchemy) -> None:
    k1: Final[orm.Key] = orm.Key(
        key_id="bc490419-7d60-487f-adc1-4ddcc177c139",
        key_material="wHHVxRwDJs3/bXd38GHP3oe4svTuRpZS0yCC7x4Ly+s="
    )

    k2: Final[orm.Key] = orm.Key(
        key_id="0a782fb5-3434-48fe-aa4d-14f41d46cf92",
        key_material="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )

    db.session.add_all([k1, k2])
    db.session.commit()
