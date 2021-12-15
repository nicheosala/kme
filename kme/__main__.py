import logging
from argparse import ArgumentParser
from typing import Final

from connexion import App as ConnexionApp

from kme import create_app
from kme.configs import Config, Development, Test, Production


def get_mode() -> Config:
    parser: Final[ArgumentParser] = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-dev', action='store_true',
                       help='Start kme in development mode.')
    group.add_argument('-prod', action='store_true',
                       help='Start kme in production mode.')
    group.add_argument('-test', action='store_true',
                       help='Start kme in test mode.')
    args = parser.parse_args()
    if args.prod:
        return Production()
    elif args.test:
        return Test()
    else:
        return Development()


def main() -> None:
    config: Final[Config] = get_mode()
    connexion_app: Final[ConnexionApp] = create_app(config)

    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    connexion_app.run(
        host=config.HOST,
        port=config.APP_PORT,
        debug=config.DEBUG,
        server='tornado'
    )


if __name__ == '__main__':
    main()
