import logging
from typing import Final

from connexion import App as ConnexionApp
from flask import Flask

from kme.configs import Config, Production, Development
from kme.database import add_database
from kme.encoder import CustomEncoder
from kme.error_handler import add_error_handlers


def create_app(config: Config = Production) -> ConnexionApp:
    # Connexion does not provide good type hints (yet). We have to consider two apps:
    # - connexion_app of type App (alias for FlaskApp), that is the actual Connexion application, managing the APIs
    # - flask_app of type Flask, that is the Flask application, embedded into the Connexion app, managing HTTP requests
    connexion_app: Final[ConnexionApp] = ConnexionApp(__name__)

    connexion_app.add_api(
        specification='api/openapi.yaml',
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )

    flask_app: Final[Flask] = connexion_app.app
    flask_app.json_encoder = CustomEncoder
    flask_app.config.from_object(config)

    add_error_handlers(flask_app)
    add_database(flask_app)

    return connexion_app


def main():
    config: Final[Config] = Development()  # TODO find a way to distinguish development and production start
    connexion_app: Final[ConnexionApp] = create_app(config)

    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    connexion_app.run(
        port=config.APP_PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
