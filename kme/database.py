from typing import Final

from databases import Database
from orm import ModelRegistry

from kme.configs import Config

database: Final[Database] = Database(
    Config.DATABASE_URL,
    check_same_thread=False,
)

models: Final[ModelRegistry] = ModelRegistry(database=database)
