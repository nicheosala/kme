from typing import Final

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: Final[SQLAlchemy] = SQLAlchemy()


def add_database(app: Flask) -> None:
    db.init_app(app=app)
    db.create_all(app=app)
