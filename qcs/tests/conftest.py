from pytest import fixture

from qcs import QCSimulator
from qcs.configs import Test


@fixture
def qc_simulator() -> QCSimulator:
    return QCSimulator(Test())
