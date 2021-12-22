from kme.configs import Config
from kme.main import create_app
from uvicorn import run

if __name__ == '__main__':
    run(
        app=create_app(),
        host=Config.HOST,
        port=Config.APP_PORT
    )
