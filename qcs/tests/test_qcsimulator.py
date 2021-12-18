from typing import Final

from qcs.client import Client
from qcs.configs import Test
from qcs.model import Request, Response, GetResponse

client: Client = Client(Test())


class TestQCS:

    def test_get_blocks(self) -> None:
        req: Final[Request] = Request(
            command="Get keys",
            attribute="",
            value=''
        )

        res: Final[Response] = client.send(req)

        assert type(res) == GetResponse
        assert len(res.blocks) == 1

    def test_get_multiple_blocks(self) -> None:
        number: int = 2
        req: Final[Request] = Request(
            command="Get keys",
            attribute="",
            value=str(number)
        )

        res: Final[Response] = client.send(req)

        assert type(res) == GetResponse
        assert len(res.blocks) == number

    def test_get_block_by_id(self) -> None:
        pass

    def test_flush_blocks(self) -> None:
        pass

    def test_delete_by_ids(self) -> None:
        pass
