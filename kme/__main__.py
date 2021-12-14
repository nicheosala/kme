import logging
from typing import Final

from connexion import App as ConnexionApp

from kme import create_app
from kme.configs import Config, Development


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
