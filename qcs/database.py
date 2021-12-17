from dataclasses import dataclass, field
from uuid import UUID

from qcs.orm import Block


@dataclass(frozen=True, slots=True)
class Database:
    blocks: dict[UUID, Block] = field(default_factory=dict)
