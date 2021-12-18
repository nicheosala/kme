from pytest import fixture

from qcs import QCSimulator
from qcs.configs import Test


@fixture(scope='module', autouse=True)
def run_qcsimulator() -> None:
    qc: QCSimulator = QCSimulator(Test())
    qc.run()
