from typing import Iterator, Final

from fastapi import FastAPI
from fastapi.testclient import TestClient as Client
from pytest import fixture
from sqlalchemy.orm import Session

from kme import create_app, orm
from kme.database import engine, SessionLocal, Base


@fixture
def app() -> Iterator[FastAPI]:
    yield create_app()


@fixture
def client(app: FastAPI) -> Client:
    return Client(app)


@fixture(autouse=True)
def session() -> Iterator[Session]:
    Base.metadata.create_all(engine)
    _session = SessionLocal()
    setup_initial_data(_session)

    yield _session

    _session.close()
    Base.metadata.drop_all(engine)


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
