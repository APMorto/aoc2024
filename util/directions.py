from enum import Enum, EnumType, IntEnum
from typing import Tuple


class Direction2D(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn_right(self):
        return Direction2D((self.value + 1) % 4)

    def turn_left(self):
        return Direction2D((self.value + 3) % 4)

    def turn_around(self):
        return Direction2D((self.value + 2) % 4)

    def offset(self):
        return ((0, 1), (1, 0), (0, -1), (-1, 0))[self.value]

def offset_2D(direction: Direction2D) -> Tuple[int, int]:
    return ((0, 1), (1, 0), (0, -1), (-1, 0))[direction.value]



