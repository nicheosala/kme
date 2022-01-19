from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Block:
    time: int
    id: UUID
    key: tuple[int, ...]
