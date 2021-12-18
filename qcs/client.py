from socket import SOCK_STREAM, AF_INET, socket
from typing import Final

from jsons import dumps, loads

from qcs.configs import Config, Test
from qcs.model import Request, Response, GetResponse


class Client:
    host: str
    port: int

    def __init__(self, config: Config):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT

    def send(self, request: Request) -> Response:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            data: Final[str] = dumps(request)

            # Connect to server and send data
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received: Final[str] = str(sock.recv(1024), "utf-8")
            response: Final[Response] = loads(
                received,
                GetResponse,
                strict=True
            )

            return response


def main() -> None:
    client: Final[Client] = Client(Test())

    req: Final[Request] = Request(
        command="Get keys",
        attribute="",
        value=''
    )

    res: Final[Response] = client.send(req)

    print(f"Request: {req}")
    print(f"Response: {res}")
    print(f"Response type: {type(res)}")


if __name__ == '__main__':
    main()
