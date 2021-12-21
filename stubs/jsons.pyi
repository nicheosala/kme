from typing import Type, TypeVar

Self = TypeVar('Self')


def dumps(
        obj: object,
        indent: int
) -> str: ...


def load(
        json_obj: object,
        cls: Type[Self],
        strict: bool
) -> Self: ...


def dump(
        obj: object,
        strip_nulls: bool,
        strict: bool,
        strip_properties: bool
) -> object: ...


def loads(
        str_: str,
        cls: Type[Self],
        strict: bool
) -> Self: ...


class DeserializationError(Exception):
    pass
