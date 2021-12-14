from typing import Final

from connexion import App
from flask_sqlalchemy import SQLAlchemy
from pytest import fixture
from webtest import TestApp

from .. import orm
from ..__main__ import create_app
from ..configs import Test
from ..database import db as _db


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


@fixture(autouse=True)
def db(app: App) -> SQLAlchemy:
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    setup_initial_data(_db)

    yield _db

    _db.session.close()
    _db.drop_all()


def setup_initial_data(db: SQLAlchemy) -> None:
    k1 = orm.Key(
        key_id="bc490419-7d60-487f-adc1-4ddcc177c139",
        key_material="wHHVxRwDJs3/bXd38GHP3oe4svTuRpZS0yCC7x4Ly+s="
    )
    k2 = orm.Key(
        key_id="0a782fb5-3434-48fe-aa4d-14f41d46cf92",
        key_material="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )

    db.session.add_all([k1, k2])
    db.session.commit()
