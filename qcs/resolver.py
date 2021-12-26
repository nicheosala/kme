from typing import Final, Callable

from qcs.commands import *
from qcs.database import Database
from qcs.model import Request, Response

db: Final[Database] = Database()

commands: Final[dict[str, Callable[[str, str, Database], Command]]] = {
    "Get keys by IDs": GetBlocksByIds,
    "Get keys": GetBlocks,
    "Flush keys": FlushBlocks,
    "Delete by IDs": DeleteBlocksByIDs
}


def resolve(request: Request) -> Response:
    return commands \
        .get(request.command, NotFound)(request.value, request.attribute, db) \
        .execute()
