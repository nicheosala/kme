from kme.configs import Config
from kme.main import app
from uvicorn import run

if __name__ == '__main__':
    run(
        app=app,
        host=Config.HOST,
        port=Config.APP_PORT
    )
