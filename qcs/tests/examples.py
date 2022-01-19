from typing import Final
from uuid import UUID

from qcs.orm import Block

block_1: Final[Block] = Block(
    time=1640034528,
    id=UUID('fa63d644-62c3-4818-a170-f3d0bd367888'),
    key=(
        189, 28, 36, 21, 180, 130, 118, 221, 89, 26, 100, 118, 171, 84, 254,
        110, 148, 170, 255, 39, 142, 235, 153, 225, 224, 252, 161, 232, 141,
        159, 210, 172
    )
)

block_2: Final[Block] = Block(
    time=1640534728,
    id=UUID('22832407-7a17-4417-a754-71e51b968889'),
    key=(
        152, 45, 15, 171, 239, 119, 71, 83, 154, 86, 18, 169, 13, 109, 37,
        238, 128, 163, 129, 126, 193, 222, 2, 48
    )
)
