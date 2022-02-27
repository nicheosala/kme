"""Representation of a Block inside the database."""
from orm import Model, Integer, UUID, JSON

from kme.database import local_models
from qcs import Block as QcsBlock


class Block(Model):  # type: ignore
    """Representation of a Block inside the database."""

    link_id: UUID
    block_id: UUID
    timestamp: int
    material: list[int]
    available_bits: int

    tablename = "blocks"
    registry = local_models
    fields = {
        "id": Integer(primary_key=True),
        "link_id": UUID(allow_null=False),
        "block_id": UUID(unique=True, allow_null=False),
        "timestamp": Integer(allow_null=False),
        "material": JSON(allow_null=False),
        "available_bits": Integer(allow_null=False),
    }

    @classmethod
    async def create_from_qcs_block(cls, qcs_block: QcsBlock) -> None:
        await cls.objects.create(
            link_id=qcs_block.link_id,
            block_id=qcs_block.id,
            material=qcs_block.key,
            timestamp=qcs_block.time,
            available_bits=len(qcs_block.key),
        )
