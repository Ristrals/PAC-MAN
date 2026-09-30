# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

from enum import Enum


class TextColors:
    """ANSI color codes for terminal output formatting.

    Attributes:
        red: Red terminal color code.
        blu: Blue terminal color code.
        grn: Green terminal color code.
        ylw: Yellow terminal color code.
        cyn: Cyan terminal color code.
        pnk: Pink terminal color code.
        org: Orange terminal color code.
        clr: Terminal color reset code.
    """
    red = '\033[91m'
    blu = '\033[94m'
    grn = '\033[92m'
    ylw = '\033[93m'
    cyn = '\033[36m'
    pnk = '\033[95m'
    org = '\033[38;2;255;165;0m'
    clr = '\033[0m'


class Movements(Enum):
    """Represent the movement directions available to token entities.

    Attributes:
        UP: Direction toward the cell above the current cell.
        DOWN: Direction toward the cell below the current cell.
        LEFT: Direction toward the cell to the left of the current cell.
        RIGHT: Direction toward the cell to the right of the current cell.
    """

    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"

    # Return the opposite direction of the current direction
    @property
    def opposite(self) -> "Movements":
        """Return the direction opposite to the current direction."""
        match self:
            case Movements.UP: return Movements.DOWN
            case Movements.DOWN: return Movements.UP
            case Movements.LEFT: return Movements.RIGHT
            case Movements.RIGHT: return Movements.LEFT

    # Return the directionnal offset of the forward cell (y, x)
    @property
    def cell_offset(self) -> tuple[int, int]:
        """Return the grid offset of the adjacent cell in this direction.

        Returns:
            A ``(y, x)`` offset for the cell ahead of the current cell.
        """
        match self:
            case Movements.UP: return -1, 0
            case Movements.DOWN: return 1, 0
            case Movements.LEFT: return 0, -1
            case Movements.RIGHT: return 0, 1

    @property
    def is_vertical(self) -> bool:
        """Return whether the direction is vertical."""
        return self in (Movements.UP, Movements.DOWN)

    @property
    def is_horizontal(self) -> bool:
        """Return whether the direction is horizontal."""
        return self in (Movements.RIGHT, Movements.LEFT)
