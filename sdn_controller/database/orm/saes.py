"""Representation of a Block inside the database."""
from orm import Model, UUID, ForeignKey, Integer

from sdn_controller.database import local_models
from sdn_controller.database.orm.kmes import Kme


class Sae(Model):  # type: ignore
    """Representation of a SAE inside the database of the SDN Controller."""

    sae_id: UUID
    kme: Kme

    tablename = "saes"
    registry = local_models
    fields = {
        "id": Integer(primary_key=True),
        "sae_id": UUID(unique=True),
        "kme": ForeignKey(Kme, allow_null=False)
    }
