from uvicorn import run

from kme import app
from kme.configs import Config

if __name__ == "__main__":
    # noinspection PyTypeChecker
    run(app=app, host=Config.HOST, port=Config.PORT)
