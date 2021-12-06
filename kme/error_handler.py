from connexion import ProblemException

from kme.models.error import Error


def render_connexion_exception(error: ProblemException) -> tuple[str, int]:
    return str({'message': error.detail}), 503


def render_model_exception(error: Error) -> tuple[str, int]:
    return str(error), error.status


def add_error_handlers(app) -> None:
    # noinspection PyTypeChecker
    app.add_error_handler(ProblemException, render_connexion_exception)
    # noinspection PyTypeChecker
    app.add_error_handler(Error, render_model_exception)
