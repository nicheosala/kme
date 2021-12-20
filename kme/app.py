from typing import Final

from connexion import App as ConnexionApp
from flask import Flask, redirect, Response

from kme.config import Config
from kme.encoder import CustomEncoder
from kme.error_handler import add_error_handlers


def create_app() -> ConnexionApp:
    # Connexion does not provide good type hints (yet). We have to consider
    # two apps:
    # - connexion_app of type App (alias for FlaskApp), that is
    # the actual Connexion application, managing the APIs
    # - flask_app of type Flask, that is the Flask application, embedded
    # into the Connexion app, managing HTTP requests
    connexion_app: Final[ConnexionApp] = ConnexionApp(__name__)

    connexion_app.add_api(
        specification=Config.API_PATH,
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )

    flask_app: Final[Flask] = connexion_app.app
    flask_app.json_encoder = CustomEncoder
    flask_app.config.from_object(Config)

    @flask_app.route('/')
    def home() -> Response:
        """Redirect to Swagger UI."""
        return redirect(f'{Config.BASE_URL}/ui/')

    add_error_handlers(flask_app)

    return connexion_app
