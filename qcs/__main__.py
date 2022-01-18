"""Start a quantum channel simulator."""
from threading import Event

from qcs import Simulator

if __name__ == '__main__':
    with Simulator():
        try:
            Event().wait()
        except KeyboardInterrupt:
            exit()
