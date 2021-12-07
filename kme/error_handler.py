from connexion import ProblemException

from kme.models.error import Error


def render_connexion_exception(error: ProblemException) -> tuple[str, int]:
    return str({'message': error.detail}), error.status if error.status < 500 else 503


def render_model_exception(error: Error) -> tuple[str, int]:
    return error.json_string, error.status


def add_error_handlers(app) -> None:
    # noinspection PyTypeChecker
    app.add_error_handler(ProblemException, render_connexion_exception)
    # noinspection PyTypeChecker
    app.add_error_handler(Error, render_model_exception)