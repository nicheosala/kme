from pytest import fixture

from qcs.qc_simulator import QCSimulator


@fixture(scope='module', autouse=True)
def run_qcsimulator() -> None:
    with QCSimulator():
        yield
