from typing import Final, Callable

from .commands.command import Command
from .commands.delete_blocks_by_ids import DeleteBlocksByIDs
from .commands.flush_blocks import FlushBlocks
from .commands.get_block_by_id import GetBlockById
from .commands.get_blocks import GetBlocks
from .commands.not_found import NotFound
from .database import Database
from .request import Request
from .response import Response

db: Final[Database] = Database()

commands: Final[dict[str, Callable[[str, str, Database], Command]]] = {
    "Get key by ID": GetBlockById,
    "Get keys": GetBlocks,
    "Flush keys": FlushBlocks,
    "Delete by IDs": DeleteBlocksByIDs
}


def resolve(request: Request) -> Response:
    return commands \
        .get(request.command, NotFound)(request.value, request.attribute, db) \
        .execute()
