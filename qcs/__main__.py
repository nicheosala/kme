"""Start a quantum channel simulator."""
from signal import pause

from qcs import Simulator

if __name__ == '__main__':
    with Simulator():
        pause()
