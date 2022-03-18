"""Configuration parameters for KME."""
from argparse import Namespace, ArgumentParser
from os import environ
from typing import Final

from kme.configs.configs import Base, Dev, Test, Prod


def read_args() -> Namespace:
    """Read parameters from CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-C",
        "--config",
        type=str,
        help="The kme id to select in the Config file.",
        default="Alice",
    )

    return parser.parse_args()


def __set_config() -> Base:
    """Initialize the configuration."""
    env: str | None = environ.get("env")
    args = read_args()
    if env == "prod":
        return Prod(args.config)
    elif env == "test":
        return Test(args.config)
    else:
        return Dev(args.config)


Config: Final[Base] = __set_config()
