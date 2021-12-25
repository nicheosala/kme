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
        obj: Self,
        cls: Type[Self],
        strip_nulls: bool,
        strict: bool,
        strip_properties: bool
) -> object: ...


def loads(
        string: str,
        cls: Type[Self],
        strict: bool
) -> Self: ...


class DeserializationError(Exception):
    pass
