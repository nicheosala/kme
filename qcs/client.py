from socket import SOCK_STREAM, AF_INET, socket
from typing import Final

from jsons import dumps, loads

from qcs.model import Request, Response, GetResponse


def send(request: Request, sock: socket) -> Response:
    data: Final[str] = dumps(request)

    # Connect to server and send data
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received: Final[str] = str(sock.recv(1024), "utf-8")
    response: Final[Response] = loads(received, GetResponse, strict=True)

    # TODO logging instead of printing
    print(f"Raw request: {data}")
    print(f"Raw response: {received}")

    return response


def get_socket() -> socket:
    return socket(AF_INET, SOCK_STREAM)


def main() -> None:
    host: Final[str] = "localhost"
    port: Final[int] = 9998

    with get_socket() as sock:
        sock.connect((host, port))

        req: Final[Request] = Request(
            command="Get keys",
            attribute="",
            value=''
        )

        res: Final[Response] = send(req, sock)

        print(f"Response type: {type(res)}")


if __name__ == '__main__':
    main()
