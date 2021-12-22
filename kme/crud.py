from typing import Final
from uuid import UUID

from sqlalchemy.orm import Session

from kme import orm
from kme.errors import KeyNotFoundError


def fetch_key(session: Session, key_id: UUID) -> orm.Key:
    key: Final[orm.Key] = session \
        .query(orm.Key) \
        .filter_by(key_id=str(key_id)) \
        .one_or_none()

    if key:
        return key

    raise KeyNotFoundError


def delete_key(session: Session, key_id: UUID) -> None:
    if orm_key := fetch_key(session, key_id):
        session.delete(orm_key)
        session.commit()
        session.refresh(orm_key)


def add_key(session: Session, key_id: UUID, key_material: str) -> orm.Key:
    orm_key: Final[orm.Key] = orm.Key(
        key_id=str(key_id),
        key_material=key_material
    )

    session.add(orm_key)
    session.commit()
    session.refresh(orm_key)

    return orm_key
