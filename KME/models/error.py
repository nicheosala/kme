from dataclasses import dataclass


@dataclass(frozen=True)
class EmptyValueError(Exception):

    def __str__(self) -> str:
        return f"Non nullable field set to `None`"


@dataclass(frozen=True)
class Error:
    message: str
    details: list[object] | None = None

    def __post_init__(self) -> None:
        if self.message is None:
            raise EmptyValueError
