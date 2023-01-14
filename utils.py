from __future__ import annotations
from enum import Enum


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)

    def is_left_turn(self, other: Direction):
        return [self, other] in [
            [Direction.UP, Direction.LEFT],
            [Direction.LEFT, Direction.DOWN],
            [Direction.DOWN, Direction.RIGHT],
            [Direction.RIGHT, Direction.UP]
        ]


def opposite(direction: Direction):
    return {
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN
    }[direction]