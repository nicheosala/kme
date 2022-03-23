"""Utility functions."""
from base64 import b64decode, b64encode
from datetime import datetime
from typing import Collection


def now() -> int:
    """Return the actual timestamp as an integer."""
    return int(datetime.now().timestamp())
