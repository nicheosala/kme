from asyncio import open_connection
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
        reader, writer = await open_connection(self.host, self.port)

        writer.write(bytes(dumps(request, indent=4) + "\n", 'utf-8'))
        await writer.drain()

        received: Final[str] = str(await reader.read(), 'utf-8')

        writer.close()
        await writer.wait_closed()

        return received
