from connexion import ProblemException
from flask import Flask

from kme.models.error import Error


def render_connexion_exception(error: ProblemException) -> tuple[str, int]:
    return str({'message': error.detail}), error.status if error.status < 500 else 503


def render_model_exception(error: Error) -> tuple[str, int]:
    return error.json_string, error.status


def add_error_handlers(app: Flask) -> None:
    app.register_error_handler(ProblemException, render_connexion_exception)
    app.register_error_handler(Error, render_model_exception)
