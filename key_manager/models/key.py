from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Key:
    """Random digital data with an associated universally unique ID."""
    key_ID: str
    key: str

    def size(self) -> int:
        return len(self.key)

    def __eq__(self, other) -> bool:
        return isinstance(other, Key) and self.key_ID == other.key_ID  # TODO ma sei sicuro? Mi sembra un po' uno schifo
