"""A simulator of a quantum key channel."""
import logging
from typing import Final

from qcs import QCSimulator
from qcs.configs import Test, Config


def main() -> None:
    config: Final[Config] = Test()  # TODO

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    qcs: Final[QCSimulator] = QCSimulator(config)
    qcs.run()


if __name__ == '__main__':
    main()
