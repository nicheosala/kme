from orm import Model, Integer, UUID, String
from kme.database import models


class Key(Model):  # type: ignore
    tablename = "keys"
    registry = models
    fields = {
        'id': Integer(primary_key=True),
        'key_id': UUID(unique=True, allow_null=False),
        'key_material': String(allow_null=False, max_length=100),
    }
