import logging
from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn
from threading import Thread
from typing import Final, Any

from jsons import loads

from qcs.configs import Config
from qcs.model import Request, Response
from qcs.resolver import resolve


class Simulator:
    """Start a Quantum Channel Simulator
    Usage:
    with Simulator():
        *do things*

    Otherwise. you can start it with .start(),
    BUT then you have to remember to close it with .stop()
    """

    def __init__(self, host: str = Config.HOST, port: int = Config.PORT):
        self.host = host
        self.port = port
        self.server = ThreadedTCPServer(
            (Config.HOST, Config.PORT),
            ThreadedTCPRequestHandler
        )

        def start_server() -> None:
            self.server.serve_forever(
                poll_interval=Config.POLL_INTERVAL
            )

        self.server_thread = Thread(
            target=start_server,
            daemon=True,
        )

    def __enter__(self) -> None:
        self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
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
    allow_reuse_address = True


class ThreadedTCPRequestHandler(StreamRequestHandler):

    def handle(self) -> None:
        data: Final[str] = self.rfile.readline().decode()
        request: Final[Request] = loads(data, Request, strict=True)

        response: Final[Response] = resolve(request)
        self.wfile.write(bytes(response.json_string, "utf-8"))

        logging.debug(f"""
        Client: {self.client_address}
        Request: {request}
        Response: {response}""")
