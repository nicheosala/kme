from socket import SOCK_STREAM, AF_INET, socket
from typing import Final

from jsons import dumps, loads

from model.request import Request
from model.response import Response


def send(request: Request, sock: socket) -> Response:
    data: Final[str] = dumps(request)

    # Connect to server and send data
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received: Final[str] = str(sock.recv(1024), "utf-8")

    # TODO logging instead of printing
    print(f"Raw request: {data}")
    print(f"Raw response: {received}")

    return loads(received, Response, strict=True)


def connect() -> socket:
    host: Final[str] = "localhost"
    port: Final[int] = 9998
    sock: Final[socket] = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    return sock


def main() -> None:
    sock: Final[socket] = connect()

    req: Final[Request] = Request(
        command="Get key by ID",
        attribute="",
        value='["18bbcdf8-189e-47e1-8119-bd5b659473f8"]'
    )

    res: Final[Response] = send(req, sock)

    sock.close()


if __name__ == '__main__':
    main()
