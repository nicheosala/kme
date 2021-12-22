from dataclasses import dataclass

from sqlalchemy import Column, String

from kme.database import Base


@dataclass
class Key(Base):  # type: ignore
    __tablename__ = "keys"

    key_id: str = Column(
        String,
        primary_key=True,
    )

    key_material: str = Column(
        String,
        nullable=False,
    )
