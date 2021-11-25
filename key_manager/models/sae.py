from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SAE:
    """Secure Application Entity"""
    id: str
