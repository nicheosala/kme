"""This is the only module allowed to communicate with the database."""
from kme.database.db import database, models
from kme.database.dbms import generate, get, delete

__all__ = [
    'database',
    'models',
    'generate',
    'get',
    'delete'
]
