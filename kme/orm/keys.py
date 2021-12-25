from orm import Model, Integer, UUID, JSON

from kme.database import models


class Key(Model):  # type: ignore
    key_id: UUID
    instructions: object

    tablename = "keys"
    registry = models
    fields = {
        'id': Integer(primary_key=True),
        'key_id': UUID(unique=True, allow_null=False),
        'instructions': JSON(allow_null=False),
    }
