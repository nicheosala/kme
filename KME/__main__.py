from json import dumps

from connexion import App, ProblemException

from KME import encoder


def render_problem_exception(error):
    return dumps({'message': error.detail}, indent="\t"), error.status


def main():
    app = App(__name__, specification_dir='../api/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        specification='swagger.yaml',
        arguments={'title': 'Key Management Entity'},
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
