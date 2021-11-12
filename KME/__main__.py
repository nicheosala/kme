from json import dumps
from typing import Final

from connexion import App, ProblemException

from KME.configs import Config, Production, Development
from KME.encoder import CustomEncoder


def render_problem_exception(error):
    return dumps({'message': error.detail}, indent="\t"), error.status


def create_app(config: Config = Production) -> App:
    app = App(__name__, server='tornado', specification_dir='../api/')
    app.app.json_encoder = CustomEncoder
    app.app.config.from_object(config)
    app.add_api(
        specification='openapi.yaml',
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )

    # noinspection PyTypeChecker
    app.add_error_handler(
        ProblemException,
        render_problem_exception
    )

    return app


def main():
    config: Final[Config] = Development()  # TODO find a way to distinguish development and production start
    app: Final[App] = create_app(config)
    app.run(
        port=config.APP_PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
