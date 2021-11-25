from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Request:
    command: str
    attribute: str
    value: str
