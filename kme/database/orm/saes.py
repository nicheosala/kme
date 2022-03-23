from orm import Integer, UUID

from kme.database import local_models


class Sae(Model):  # type: ignore
    """Representation of a SAE inside the database of the KME."""

    sae_id: UUID

    tablename = "saes"
    registry = local_models
    fields = {
        "id": Integer(primary_key=True),
        "sae_id": UUID(unique=True),
    }
