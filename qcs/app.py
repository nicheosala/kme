from typing import Final

from jsons import loads, dumps

from socketserver import TCPServer, StreamRequestHandler
import logging

from qcs.configs import Config
from qcs.model import Request, Response
from qcs.resolver import resolve


class QCSimulator:
    host: str
    port: int
    server: TCPServer

    def __init__(self, config: Config):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT
        self.server = TCPServer((self.host, self.port), MyTCPHandler)

    def run(self) -> None:
        with self.server as server:
            logging.info(f"Server listening on {self.host}:{self.port}")
            server.serve_forever()


class MyTCPHandler(StreamRequestHandler):

    def handle(self) -> None:
        data: Final[str] = self.rfile.readline().decode()
        request: Final[Request] = loads(data, Request, strict=True)

        response: Final[Response] = resolve(request)
        self.wfile.write(bytes(dumps(response), "utf-8"))

        logging.debug(f"""
        Client: {self.client_address}
        Request: {request}
        Response: {response}""")
