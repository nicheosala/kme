"""Representation of a Key stream between two saes inside the database."""
import orm
from orm import Model, UUID, ForeignKey, Integer, JSON

from sdn_controller.database.db import local_models
from sdn_controller.database.orm.kmes import Kme
from sdn_controller.database.orm.saes import Sae


class Ksid(Model):  # type: ignore
    """Representation of a Key stream between two saes inside the database of the SDN Controller."""

    key_stream_id: UUID
    sae1: Sae
    sae2: Sae
    kme1: Kme
    kme2: Kme
    qos: dict[str, int | bool]

    tablename = "ksids"
    registry = local_models
    fields = {
        "id": Integer(primary_key=True),
        "key_stream_id": UUID(unique=True, allow_null=True),
        "sae1": ForeignKey(Sae, allow_null=False, on_delete=orm.CASCADE),
        "sae2": ForeignKey(Sae, allow_null=True, on_delete=orm.CASCADE),
        "kme1": ForeignKey(Kme, allow_null=False, on_delete=orm.CASCADE),
        "kme2": ForeignKey(Kme, allow_null=True, on_delete=orm.CASCADE),
        "qos": JSON(allow_null=False)
    }
