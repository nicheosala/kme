from typing import Final

from sqlalchemy.future import Engine, create_engine
from sqlalchemy.orm import Session, registry, DeclarativeMeta

from kme.configs import Config

engine: Final[Engine] = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=Config.DEBUG,
    future=Config.SQLALCHEMY_WARN_20
)

session: Final[Session] = Session(
    engine,
    future=Config.SQLALCHEMY_WARN_20
)

mapper_registry: Final[registry] = registry()
Base: Final[DeclarativeMeta] = mapper_registry.generate_base()


def init_database() -> None:
    mapper_registry.metadata.create_all(engine)
