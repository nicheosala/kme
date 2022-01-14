"""A simulator of a quantum channel."""
import logging
from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn
from struct import unpack, pack
from threading import Thread
from typing import Final, Any

from jsons import loads

from qcs.configs import Config
from qcs.model import Request, Response
from qcs.resolver import resolve


class Simulator:
    """Start a Quantum Channel Simulator.

    Usage:
    with Simulator():
        *do things*

    Otherwise. you can start it with .start(),
    BUT then you have to remember to close it with .stop()
    """

    def __init__(self, host: str = Config.HOST, port: int = Config.PORT):
        """Initialize the simulator."""
        self.host = host
        self.port = port
        self.server = ThreadedTCPServer(
            (Config.HOST, Config.PORT), ThreadedTCPRequestHandler
        )

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
        logging.info(f"Server listening on {self.host}:{self.port}")

    def stop(self) -> None:
        """Stop the QC Simulator.

        If you stop the QCS calling .stop() directly, before you must
        have explicitly started it with a call to .start(). For this reason,
        usage with the 'with' statement should be preferred.
        """
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
        logging.info(f"Server shutdown completed.")


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """Provide thread anc TCP functionlaities to the simulator."""

    allow_reuse_address = True


class ThreadedTCPRequestHandler(StreamRequestHandler):
    """Class for handling TCP requests."""

    def handle(self) -> None:
        """Handle a TCP request."""
        len_data: Final[int] = unpack(">I", self.rfile.read(4))[0]
        data: Final[str] = self.rfile.read(len_data).decode()

        request: Final[Request] = loads(data, Request, strict=True)

        response: Final[Response] = resolve(request)

        len_response: Final[int] = len(response.json_string)
        self.wfile.write(pack(">I", len_response))
        self.wfile.write(bytes(response.json_string, "utf-8"))

        logging.info(
            f"""
        Client: {self.client_address}
        Request: {request}
        Response: {response}"""
        )
