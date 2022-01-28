"""The server listening to new blocks from the quantum channel."""
import asyncio
import logging
from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn
from struct import unpack
from threading import Thread
from typing import Final, Any

from jsons import loads

from kme.configs import Config
from kme.database import orm
from qcs import Block


class QCServer:
    """The server listening to new blocks from the quantum channel.

    Usage:
    with QCServer():
        *do things*

    Otherwise, you can start it with .start(),
    BUT then you have to remember to close it calling .stop()
    """

    def __init__(self, host: str = Config.HOST, port: int = Config.QC_PORT):
        """Initialize the server."""
        self.host = host
        self.port = port
        self.server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)

        def start_server() -> None:
            self.server.serve_forever(poll_interval=Config.POLL_INTERVAL)

        self.server_thread = Thread(
            target=start_server,
            daemon=True,
        )

    def __enter__(self) -> None:
        """Start the simulator."""
        self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop the simulator."""
        self.stop()

    def start(self) -> None:
        """Start the QC Simulator.

        If you start the QCS calling .start() directly, then you must
        explicitly stop it with a call to .stop(). For this reason, usage with
        the 'with' statement should be preferred.
        """
        self.server_thread.start()
        logging.getLogger("kme").info(f"QCServer listening on {self.host}:{self.port}")

    def stop(self) -> None:
        """Stop the QC Simulator.

        If you stop the QCS calling .stop() directly, before you must
        have explicitly started it with a call to .start(). For this reason,
        usage with the 'with' statement should be preferred.
        """
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
        logging.getLogger("kme").info(f"QCServer shutdown completed.")


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Provide thread anc TCP functionalities to the QCServer."""

    allow_reuse_address = True


class ThreadedTCPRequestHandler(StreamRequestHandler):
    """Class for handling TCP requests."""

    def handle(self) -> None:
        """Handle a TCP request."""
        len_data: Final[int] = unpack(">I", self.rfile.read(4))[0]
        data: Final[str] = self.rfile.read(len_data).decode()

        new_block: Final[Block] = loads(data, Block, strict=True)

        asyncio.run(add_block(new_block))

        logging.getLogger("kme").debug(f"Received new block with id {new_block.id}")


async def add_block(new_block: Block) -> None:
    """Add newly-generated block to database."""
    await orm.Block.objects.create(
        block_id=new_block.id,
        material=new_block.key,
        timestamp=new_block.time,
        available_bits=len(new_block.key),
    )
