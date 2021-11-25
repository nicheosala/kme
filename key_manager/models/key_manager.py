from dataclasses import dataclass
from typing import Final

from .key import Key


def key_gen(size: int) -> str:
    """Retrieve key from underlying hardware."""
    pass


def id_gen() -> str:
    """Get a new uuid for a key"""
    pass


@dataclass(frozen=True, slots=True)
class KeyManager:  # TODO this must be a singleton
    keys: dict[str, str]  # key_id, (key, sae_ids)

    def get(self, key_id: str) -> Key:
        """Get the keys associated to the given SAE ID"""
        if key_id in self.keys:
            return Key(key_id, self.keys[key_id])
        else:
            raise Exception

    def generate(self, size: int, sae_ids: tuple[str]) -> Key:
        """Generate a new random key"""
        new_id: Final[str] = id_gen()
        new_key: Final[str] = key_gen(size)
        self.keys[new_id] = new_key
        return Key(new_id, new_key)

    def remove(self, key_id: str) -> None:
        self.keys.pop(key_id)
