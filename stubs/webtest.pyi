from typing import Any

from flask import Flask


class TestApp:

    def __init__(
            self,
            app: Flask
    ) -> None: ...

    def get(
            self,
            url: str,
            params: dict[str, Any] | None = None,
            expect_errors: bool = False
    ) -> TestResponse: ...

    def post(
            self,
            url: str,
            params: str,
            content_type: str,
            expect_errors: bool
    ) -> TestResponse: ...


class TestResponse:
    json_body: object
    status_int: int
