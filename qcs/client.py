from socket import SOCK_STREAM, AF_INET, socket
from typing import Final

from jsons import dumps

from qcs.configs import Config
from qcs.model import Request


class Client:
    host: str
    port: int

    def __init__(self, config: Config):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT

    async def send(self, request: Request) -> str:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            data: Final[str] = dumps(request, indent=4)

            # Connect to server and send data
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            return str(sock.recv(4096), "utf-8")
            # TODO the size of the buffer cannot be left hardcoded. It must
            #  be handled better. What if the client ask for 60 blocks?
