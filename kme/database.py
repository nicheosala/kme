from typing import Final

from connexion import App
from flask_sqlalchemy import SQLAlchemy

db: Final[SQLAlchemy] = SQLAlchemy()


def _init_db(self: SQLAlchemy, app=None):
    self.create_all(app=app)


db.init_db = type(db.init_app)(_init_db, db)


def add_database(app: App) -> None:
    db.init_app(app.app)
    db.init_db(app.app)
