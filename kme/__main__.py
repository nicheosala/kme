import logging
from typing import Final

from connexion import App

from kme.configs import Config, Production, Development
from kme.database import add_database
from kme.encoder import CustomEncoder
from kme.error_handler import add_error_handlers


def create_app(config: Config = Production) -> App:
    app = App(__name__, server='tornado', specification_dir='api/')
    app.app.json_encoder = CustomEncoder
    app.app.config.from_object(config)
    app.add_api(
        specification='openapi.yaml',
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )

    add_error_handlers(app)
    add_database(app)

    return app


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
