"""A quantum channel simulator."""
import configparser
import logging
import os
from argparse import Namespace, ArgumentParser
from asyncio import open_connection, sleep, run
from dataclasses import dataclass
from datetime import datetime
from struct import pack
from typing import Final
from uuid import uuid4

from jsons import dumps

from qcs import Block


@dataclass
class KME:
    """A KME (host, port) couple."""

    host: str
    port: int


KME_A = KME("localhost", 9998)
KME_B = KME("localhost", 9999)
KMEs = (KME_A, KME_B)

DEBUG: bool = True
GEN_INTERVAL: int = 5
LINK_ID = uuid4()


def timestamp() -> int:
    """The current integer timestamp."""
    return int(datetime.now().timestamp())


def get_random_bits() -> tuple[int, ...]:
    """Simulate the generation of a random number of bits.

    More precisely, a random number of bytes, each constituted by 8 random
    bits, is returned. The randomness is simulated exploiting Python's
    "random" library.

    :return: a tuple, containing a random number of random bytes.
    """
    from random import getrandbits, randint

    lb, ub = 1000, 2000  # Generate a number of random bytes btw [lb, ub].
    return tuple(getrandbits(8) for _ in range(randint(lb, ub)))


async def send(block: Block, kme: KME) -> None:
    """Send to the key kme a newly-generated block."""
    _, writer = await open_connection(kme.host, kme.port)

    message: Final[str] = dumps(block, indent=4) + "\n"
    len_message: Final[int] = len(message)

    writer.write(pack(">I", len_message))
    await writer.drain()

    writer.write(bytes(message, "utf-8"))
    await writer.drain()

    writer.close()
    await writer.wait_closed()


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("qcs")
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


def read_args() -> Namespace:
    """Read parameters from CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-C",
        "--config",
        type=str,
        help="The two sd_qkd_node ids to which the qcs is referred.",
        default="Alice-Bob",
    )

    return parser.parse_args()


# Check Config file for info
def set_params(served_nodes: str = "Alice-Bob") -> None:
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
    upper_nodes = served_nodes.upper()
    global KME_A, KME_B, DEBUG, GEN_INTERVAL, KMEs
    KME_A = KME(config[upper_nodes]["KME_A_IP"], int(config[upper_nodes]["KME_A_PORT"]))
    KME_B = KME(config[upper_nodes]["KME_B_IP"], int(config[upper_nodes]["KME_B_PORT"]))
    DEBUG = bool(config["SHARED"]["DEBUG"])
    GEN_INTERVAL = int(config["SHARED"]["GEN_INTERVAL"])
    KMEs = (KME_A, KME_B)


async def main() -> None:
    """Main function."""
    set_logging()
    args = read_args()
    set_params(args.config)

    while True:
        await sleep(GEN_INTERVAL)

        new_block = Block(timestamp(), uuid4(), get_random_bits(), LINK_ID)
        logging.getLogger("qcs").info(f"New block generated with ID {new_block.id}")

        for kme in KMEs:
            await send(new_block, kme)


if __name__ == "__main__":
    run(main())
