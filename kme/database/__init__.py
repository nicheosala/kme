"""This is the only module allowed to communicate with the database."""
from kme.database.db import local_db, local_models, shared_db, shared_models
from kme.database.dbms import generate, get, delete, get_block_by_id

__all__ = [
    "local_db",
    "local_models",
    "shared_db",
    "shared_models",
    "generate",
    "get",
    "delete",
    "get_block_by_id",
]
