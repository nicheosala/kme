"""Representation of a Key stream between two SAEs inside the database of the KME."""
from orm import Model, UUID, Integer, JSON

from sd_qkd_node.database import local_models


class Ksid(Model):  # type: ignore
    """Representation of a Key stream between two SAEs inside the database of the KME."""

    ksid: UUID
    src: UUID
    dst: UUID
    kme_src: UUID
    kme_dst: UUID
    qos: dict[str, int | bool]

    tablename = "ksids"
    registry = local_models
    fields = {
        # TODO dk why if ksid pk, when create a Ksid in the db, assigning the ksid gives NOT NULL constraint violated
        "id": Integer(primary_key=True),
        "ksid": UUID(unique=True, allow_null=False),
        "src": UUID(unique=True, allow_null=False),
        "dst": UUID(unique=True, allow_null=False),
        "kme_src": UUID(unique=False, allow_null=False),
        "kme_dst": UUID(unique=False, allow_null=False),
        "qos": JSON(allow_null=False)
    }
