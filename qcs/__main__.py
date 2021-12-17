"""A simulator of a quantum key channel."""
import logging
from socketserver import TCPServer, StreamRequestHandler
from typing import Final

from jsons import loads, dumps

from qcs.model import Request, Response
from qcs.resolver import resolve


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


if __name__ == '__main__':
    host: Final[str] = "localhost"
    port: Final[int] = 9998

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    with TCPServer((host, port), MyTCPHandler) as server:
        logging.info(f"Server listening on {host}:{port}")
        server.serve_forever()
