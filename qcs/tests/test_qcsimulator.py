from typing import Final

from qcs.configs import Test
from qcs.model import GetResponse
from qcs.qc_interface import QCInterface

qc_interface: Final[QCInterface] = QCInterface(Test())


class TestQCS:

    def test_get_blocks(self) -> None:
        res: Final[GetResponse] = qc_interface.get_blocks()

        assert len(res.blocks) == 1

    def test_get_multiple_blocks(self) -> None:
        number: int = 2
        res: Final[GetResponse] = qc_interface.get_blocks(number)

        assert len(res.blocks) == number

    def test_get_block_by_id(self) -> None:
        pass

    def test_flush_blocks(self) -> None:
        pass

    def test_delete_by_ids(self) -> None:
        pass
