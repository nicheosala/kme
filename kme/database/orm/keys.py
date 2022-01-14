"""Representation of a Key inside the database."""
from orm import Model, Integer, UUID, JSON

from kme.database import models


class Key(Model):  # type: ignore
    """Representation of a Key inside the database."""

    key_id: UUID
    instructions: object

    tablename = "keys"
    registry = models
    fields = {
        "id": Integer(primary_key=True),
        "key_id": UUID(unique=True, allow_null=False),
        "instructions": JSON(allow_null=False),
    }
