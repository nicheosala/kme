import logging
from datetime import datetime
from typing import Final
from uuid import uuid4

from qcs.commands import Command
from qcs.model import Response, EmptyResponse, GetResponse
from qcs.orm import Block


def _get_random_bits() -> tuple[int, ...]:
    """Simulate the generation of a random number of bits.

    More precisely, a random number of bytes, each constituted by 8 random
    bits, is returned. The randomness is simulated exploiting Python's
    "random" library.

    :return: a tuple, containing a random number of random bytes.
    """
    from random import getrandbits, randint
    lb: Final[int] = 10
    ub: Final[int] = 50
    return tuple(getrandbits(8) for _ in range(randint(lb, ub)))


def _timestamp() -> int:
    """
    :return: the current integer timestamp.
    """
    return int(datetime.now().timestamp())


class GetBlocks(Command):

    def execute(self) -> Response:
        try:
            if self.value == "":  # i.e. request.value is empty
                logging.info(f"request.value is empty: default to 1.")
                return self._gen_blocks(1)
            elif (n := int(self.value)) <= 0:
                logging.error(
                    f"request.value must be a positive integer. "
                    f"Given: {self.value}")
                return EmptyResponse()  # TODO
            else:
                return self._gen_blocks(n)
        except ValueError:
            logging.error(
                f"request.value cannot be interpreted as an integer. "
                f"Given: {self.value}")
            return EmptyResponse()  # TODO

    def _generate_block(self) -> Block:
        """Simulate the generation of a block of random bits.

        :return: a Block object containing (simulated) random bits.
        """
        new_block: Final[Block] = Block(_timestamp(), uuid4(),
                                        _get_random_bits())
        self.database.blocks[new_block.id] = new_block

        logging.debug(f"New block generated with ID {new_block.id}")

        return new_block

    def _gen_blocks(self, n: int) -> Response:
        """
        :param n: number of blocks requested by the key manager. Default value
         is 1.
        :return: Response object containing up to n blocks.
        """
        return GetResponse(tuple(self._generate_block() for _ in range(n)))
