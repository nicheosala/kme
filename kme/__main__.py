import logging
from argparse import ArgumentParser, Namespace

from uvicorn import run

from kme import app
from kme.channel.qc_server import QCServer
from kme.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("kme")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


def read_args() -> Namespace:
    """Read parameters from CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        help="The host address where kme will run.",
        default=Config.HOST,
    )
    parser.add_argument(
        "-P",
        "--port",
        type=int,
        help="The port where kme will run.",
        default=Config.PORT,
    )

    return parser.parse_args()


if __name__ == "__main__":
    set_logging()
    args = read_args()
    with QCServer():
        # noinspection PyTypeChecker
        run(app=app, host=args.host, port=args.port)
