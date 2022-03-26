"""Representation of a Key inside the database."""
import uuid

from orm import Model, UUID, String, Integer

from sdn_controller.configs import Config
from sdn_controller.database.db import local_models


class Kme(Model):  # type: ignore
    """Representation of a KME inside the database of the SDN Controller."""

    kme_id: UUID
    ip: str  # TODO can be IPAddress
    port: int

    tablename = "kmes"
    registry = local_models
    fields = {
        "kme_id": UUID(primary_key=True, default=uuid.uuid4),
        # if debugging or testing the IP will be 'localhost', then not unique
        "ip": String(unique=not(Config.DEBUG or Config.TESTING), allow_null=False, max_length=15),
        "port": Integer(allow_null=False)
    }
