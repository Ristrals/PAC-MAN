# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

from enum import Enum


class TextColors:
    """ANSI color codes for terminal output formatting."""
    red = '\033[91m'
    blu = '\033[94m'
    grn = '\033[92m'
    ylw = '\033[93m'
    cyn = '\033[36m'
    pnk = '\033[95m'
    org = '\033[38;2;255;165;0m'
    clr = '\033[0m'


class Movements(Enum):
    """Movements possible for token entity"""
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"

    # Return the opposite direction of the current direction
    @property
    def opposite(self) -> "Movements":
        match self:
            case Movements.UP: return Movements.DOWN
            case Movements.DOWN: return Movements.UP
            case Movements.LEFT: return Movements.RIGHT
            case Movements.RIGHT: return Movements.LEFT

    # Return the directionnal offset of the forward cell (y, x)
    @property
    def cell_offset(self) -> tuple[int, int]:
        match self:
            case Movements.UP: return -1, 0
            case Movements.DOWN: return 1, 0
            case Movements.LEFT: return 0, -1
            case Movements.RIGHT: return 0, 1

    @property
    def is_vertical(self) -> bool:
        return self in (Movements.UP, Movements.DOWN)

    @property
    def is_horizontal(self) -> bool:
        return self in (Movements.RIGHT, Movements.LEFT)
