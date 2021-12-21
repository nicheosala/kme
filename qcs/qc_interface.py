from typing import Final
from uuid import UUID

from jsons import dumps

from qcs.client import Client
from qcs.configs import Config
from qcs.model import Request, GetResponse
from qcs.model.response import DeleteResponse


class QCInterface:
    config: Config
    qc_client: Client

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = Client(config)

    def get_blocks(self, number: int = 1) -> GetResponse:
        req: Final[Request] = Request(
            command="Get keys",
            attribute="",
            value=str(number)
        )

        received: Final[str] = self.client.send(req)

        res: Final[GetResponse] = GetResponse.from_json(received)

        return res

    def delete_blocks(self, ids: tuple[UUID, ...]) -> DeleteResponse:
        req: Final[Request] = Request(
            command="Delete by IDs",
            attribute="",
            value=dumps(ids, indent=4)
        )

        received: Final[str] = self.client.send(req)

        res: Final[DeleteResponse] = DeleteResponse.from_json(received)

        return res

    def flush_blocks(self) -> DeleteResponse:
        req: Final[Request] = Request(
            command="Flush keys",
            attribute="",
            value=""
        )

        received: Final[str] = self.client.send(req)

        res: Final[DeleteResponse] = DeleteResponse.from_json(received)
        # TODO This does not respect the specs. The specs does not clarify
        #  what to do in this situation.

        return res
