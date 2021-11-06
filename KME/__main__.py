#!/usr/bin/env python3

import connexion

from KME import encoder


def main():
    app = connexion.App(__name__, specification_dir='../api/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        specification='swagger.yaml',
        arguments={'title': 'Key Management Entity'},
        pythonic_params=True,
        strict_validation=True,
        validate_responses=True,
    )
    app.run(host="localhost", port=8080)


if __name__ == '__main__':
    main()
