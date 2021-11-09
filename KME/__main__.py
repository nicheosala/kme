from json import dumps

from connexion import App, ProblemException

from KME.encoder import CustomEncoder


def render_problem_exception(error):
    return dumps({'message': error.detail}, indent="\t"), error.status


def main():
    app = App(__name__, server='tornado', specification_dir='../api/')
    app.app.json_encoder = CustomEncoder
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

    app.run()


if __name__ == '__main__':
    main()
