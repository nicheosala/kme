from flask import Flask


class ProblemException(Exception):
    status: int
    detail: str


class App:
    app: Flask

    def __init__(
            self,
            import_name: str
    ) -> None: ...

    def add_api(
            self,
            specification: str,
            pythonic_params: bool,
            strict_validation: bool,
            validate_responses: bool,
    ) -> None: ...

    def run(
            self,
            port: int,
            server: str,
            debug: bool,
            host: str,
    ) -> None: ...
