from threading import Thread
from typing import Final

from jsons import loads

from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn
import logging

from qcs.configs import Config
from qcs.model import Request, Response
from qcs.resolver import resolve


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True


class QCSimulator:
    host: str
    port: int

    def __init__(self, config: Config):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT

    def run(self) -> None:
        server = ThreadedTCPServer(
            (self.host, self.port),
            ThreadedTCPRequestHandler
        )
        server_thread = Thread(
            target=server.serve_forever,
            daemon=True
        )
        server_thread.start()
        logging.info(f"Server listening on {self.host}:{self.port}")


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