"""Representation of a Key inside the database."""

from orm import Model, UUID, String, Integer, IPAddress

from sdn_controller.database.db import local_models


class Kme(Model):  # type: ignore
    """Representation of a KME inside the database of the SDN Controller."""

    kme_id: UUID
    ip: str  # TODO can be IPAddress
    port: int

    tablename = "kmes"
    registry = local_models
    fields = {
        "id": Integer(primary_key=True),
        "kme_id": UUID(unique=True, allow_null=False),
        "ip": String(allow_null=False, max_length=15),
        "port": Integer(allow_null=False)
    }
