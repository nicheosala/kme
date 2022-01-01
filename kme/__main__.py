from uvicorn import run

from kme import app
from kme.configs import Config
from qcs import Simulator

if __name__ == "__main__":
    with Simulator():
        # noinspection PyTypeChecker
        run(app=app, host=Config.HOST, port=Config.PORT)
