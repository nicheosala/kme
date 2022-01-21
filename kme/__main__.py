from argparse import ArgumentParser

from uvicorn import run

from kme import app
from kme.configs import Config

if __name__ == "__main__":
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

    args = parser.parse_args()
    # noinspection PyTypeChecker
    run(app=app, host=args.host, port=args.port)
