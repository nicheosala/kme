"""Manage sending requests and receiving responses to/from the quantum channel."""
from asyncio import open_connection
from struct import pack, unpack
from typing import Final

from jsons import dumps

from qcs.configs import Config
from qcs.model import Request


async def send(request: Request) -> str:
    """Send a request to the quantum channel and return a response."""
    reader, writer = await open_connection(Config.HOST, Config.PORT)

    message: Final[str] = dumps(request, indent=4) + "\n"
    len_message: Final[int] = len(message)

    writer.write(pack(">I", len_message))
    await writer.drain()

    writer.write(bytes(message, "utf-8"))
    await writer.drain()

    len_received: Final[int] = unpack(">I", await reader.read(4))[0]
    received: Final[str] = str(await reader.read(len_received), "utf-8")

    writer.close()
    await writer.wait_closed()

    return received
