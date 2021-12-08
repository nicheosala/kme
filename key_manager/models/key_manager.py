from dataclasses import dataclass, field
from typing import Any

from immutabledict import immutabledict

from kme.models.key import Key as API_Key


def key_gen(size: int) -> tuple[str, str]:
    """Retrieve key from underlying hardware."""
    return "3fa85f64-5717-4562-b3fc-2c963f66afa6", "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    # TODO this is example key material! You have to ask the quantum channel for a new key.


@dataclass(frozen=True, slots=True)
class KeyManager:
    keys: dict[str, str] = field(default_factory=dict)  # key_id, (key, sae_ids)

    def get(self, key_id: str, master_sae_id: str) -> API_Key:
        """Get the keys associated to the given SAE ID"""
        return API_Key("3fa85f64-5717-4562-b3fc-2c963f66afa6", "OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA=")

    # TODO this is example key material!

    def remove(self, key_id: str) -> None:
        self.keys.pop(key_id)

    def generate(self, size: int, slave_sae_ids: frozenset[str], *params: immutabledict[str, Any]) -> API_Key:
        """Generate one new random key."""
        new_id, new_key = key_gen(size)
        print(slave_sae_ids)
        print(params)
        self.keys[new_id] = new_key  # TODO
        return API_Key(new_id, new_key)
