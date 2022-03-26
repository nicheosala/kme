"""Representation of a Key stream between two SAEs inside the database."""
import uuid

from orm import Model, UUID, JSON

from sdn_controller.database.db import local_models


class Ksid(Model):  # type: ignore
    """Representation of a Key stream between two SAEs inside the database of the SDN Controller."""

    ksid: UUID
    src: UUID
    dst: UUID
    kme_src: UUID
    kme_dst: UUID
    qos: dict[str, int | bool]

    tablename = "ksids"
    registry = local_models
    fields = {
        "ksid": UUID(primary_key=True, default=uuid.uuid4),
        "src": UUID(unique=True, allow_null=False),
        "dst": UUID(unique=True, allow_null=False),
        "kme_src": UUID(unique=False, allow_null=True),
        "kme_dst": UUID(unique=False, allow_null=True),
        "qos": JSON(allow_null=False)
    }
