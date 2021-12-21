import logging
from typing import Final

from connexion import App as ConnexionApp

from kme import create_app
from kme.configs import Config
from kme.database import init_database


def main() -> None:
    init_database()

    connexion_app: Final[ConnexionApp] = create_app()

    logging.basicConfig(
        level=logging.DEBUG if Config.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    connexion_app.run(
        host=Config.HOST,
        port=Config.APP_PORT,
        debug=Config.DEBUG,
        server='tornado'
    )


if __name__ == '__main__':
    main()
