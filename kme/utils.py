"""Utility functions."""
from base64 import b64decode, b64encode
from datetime import datetime
from typing import Collection


def b64_to_tupleint(b64_string: str) -> tuple[int, ...]:
    """Convert a base64 string into a tuple of integer in [0, 255]."""
    assert is_base64(b64_string)
    return tuple(b for b in b64decode(b64_string))


def collecitonint_to_b64(c: Collection[int]) -> str:
    """Convert a collection of integer in [0, 255] into a base64 string."""
    assert all(n in range(0, 256) for n in c)
    return str(b64encode(bytes(c)), "utf-8")


def bit_length(c: Collection[int]) -> int:
    """Return number of bits represented by the given collection of integer.

    Each positive integer number is considered 8-bits long, in range [0, 255].
    """
    assert all(n in range(0, 256) for n in c)
    return len(c) * 8


def bit_length_b64(b64_string: str) -> int:
    """Return the number of bits represented by the given base64 string."""
    assert is_base64(b64_string)
    return bit_length(b64_to_tupleint(b64_string))


def is_base64(s: str) -> bool:
    """Return True if 's' is a valid base64 string, else False."""
    bytes_s = bytes(s, "ascii")
    return bytes_s == b64encode(b64decode(bytes_s))


def now() -> int:
    """Return the actual timestamp as an integer."""
    return int(datetime.now().timestamp())
