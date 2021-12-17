from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Block:
    time: int
    ID: UUID
    Key: tuple[int, ...]
