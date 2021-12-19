from typing import Final

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

    def delete_blocks(self) -> DeleteResponse:
        pass  # TODO
