import logging
from typing import Final

from connexion import App
from flask import Flask

from kme.configs import Config, Production, Development
from kme.database import add_database
from kme.encoder import CustomEncoder
from kme.error_handler import add_error_handlers


def create_app(config: Config = Production) -> App:
    connexion_app: Final[App] = App(__name__, specification_dir='api/')

    connexion_app.add_api(
        specification='openapi.yaml',
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )

    add_error_handlers(connexion_app)

    flask_app: Final[Flask] = connexion_app.app
    flask_app.json_encoder = CustomEncoder
    flask_app.config.from_object(config)
    add_database(flask_app)

    return connexion_app


def main():
    config: Final[Config] = Development()  # TODO find a way to distinguish development and production start
    app: Final[App] = create_app(config)

    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    app.run(
        port=config.APP_PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
