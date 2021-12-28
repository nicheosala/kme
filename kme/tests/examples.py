"""Examples exploited for testing purposes."""
from typing import Final
from uuid import UUID

from kme import orm

key_1: Final[orm.Key] = orm.Key(
    key_id=UUID("bc490419-7d60-487f-adc1-4ddcc177c139"),
    instructions=[{
        'block_id': 'fa63d644-62c3-4818-a170-f3d0bd367888',
        'start': 0, 'end': 32
    }])

key_2: Final[orm.Key] = orm.Key(
    key_id=UUID("0a782fb5-3434-48fe-aa4d-14f41d46cf92"),
    instructions=[{
        'block_id': '22832407-7a17-4417-a754-71e51b968889',
        'start': 0, 'end': 8
    }])
