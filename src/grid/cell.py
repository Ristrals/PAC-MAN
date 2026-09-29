"""Cell model of the maze grid."""

from dataclasses import dataclass
from src.data_lib import Movements as Mvt
from enum import Enum


class StateType(Enum):
    """Content of a cell.

    Attributes:
        EMPTY: The cell contains nothing.
        SUPER_PACGUM: The cell contains a super pacgum.
        PACGUM: The cell contains a regular pacgum.
    """

    EMPTY = "empty"
    SUPER_PACGUM = "super_pacgum"
    PACGUM = "pacgum"


@dataclass
class Cell:
    """A single cell of the maze.

    Each direction flag tells whether the cell is open on that side,
    i.e. ``True`` means there is no wall and the cell can be exited
    in that direction.

    Attributes:
        x: Column index of the cell.
        y: Row index of the cell.
        north: Whether the north side is open.
        east: Whether the east side is open.
        south: Whether the south side is open.
        west: Whether the west side is open.
        state_type: Content of the cell. Defaults to ``StateType.EMPTY``.
    """

    x: int
    y: int
    north: bool
    east: bool
    south: bool
    west: bool
    state_type: StateType = StateType.EMPTY

    @property
    def coordinates(self) -> tuple[int, int]:
        """tuple[int, int]: Grid coordinates of the cell as ``(y, x)``."""
        return self.y, self.x

    @property
    def center_coord(self) -> tuple[float, float]:
        """tuple[float, float]: Center of the cell as ``(y, x)``."""
        return self.y + 0.5, self.x + 0.5

    def can_exit(self, direction: Mvt | None) -> bool:
        """Check whether the cell can be exited in the given direction.

        Args:
            direction: Direction of the movement, or ``None``.

        Returns:
            True if the side matching ``direction`` is open, False
            otherwise or if ``direction`` is ``None`` or unknown.
        """
        match direction:
            case Mvt.UP: return self.north
            case Mvt.DOWN: return self.south
            case Mvt.LEFT: return self.west
            case Mvt.RIGHT: return self.east
            case _: return False


def create_cell(x: int, y: int, value: int) -> Cell:
    """Build a cell from its encoded wall value.

    The value is a 4-bit mask where a set bit means a wall:
    bit 0 (1) is north, bit 1 (2) is east, bit 2 (4) is south and
    bit 3 (8) is west.

    Args:
        x: Column index of the cell.
        y: Row index of the cell.
        value: Bit mask encoding the walls around the cell.

    Returns:
        The new cell, with its content set to ``StateType.EMPTY``.
    """
    return Cell(
        x=x,
        y=y,
        north=not bool(value & 1),
        east=not bool(value & 2),
        south=not bool(value & 4),
        west=not bool(value & 8),
    )
