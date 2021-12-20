from typing import Final

from sqlalchemy.future import Engine, create_engine
from sqlalchemy.orm import Session, registry, DeclarativeMeta

from kme.configs import Config

engine: Final[Engine] = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=Config.DEBUG,
    future=True
)

session: Final[Session] = Session(engine, future=True)

mapper_registry = registry()
Base: Final[DeclarativeMeta] = mapper_registry.generate_base()


def add_database() -> None:
    mapper_registry.metadata.create_all(engine)
