"""Representation of a Block inside the database."""
from orm import Model, Integer, UUID, JSON

from kme.database import models


class Block(Model):  # type: ignore
    """Representation of a Block inside the database."""

    block_id: UUID
    timestamp: int
    material: list[int]
    available_bits: int

    tablename = "blocks"
    registry = models
    fields = {
        "id": Integer(primary_key=True),
        "block_id": UUID(unique=True, allow_null=False),
        "timestamp": Integer(allow_null=False),
        "material": JSON(allow_null=False),
        "available_bits": Integer(allow_null=False),
    }
