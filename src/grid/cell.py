from dataclasses import dataclass
from src.data_lib import Movements as Mvt
from enum import Enum


class StateType(Enum):
    EMPTY = "empty"
    SUPER_PACGUM = "super_pacgum"
    PACGUM = "pacgum"


@dataclass
class Cell:
    x: int
    y: int
    north: bool
    east: bool
    south: bool
    west: bool
    state_type: StateType = StateType.EMPTY

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.y, self.x

    # Return if the cell be exited in gived direction
    def can_exit(self, direction: Mvt | None) -> bool:
        match direction:
            case Mvt.UP: return self.north
            case Mvt.DOWN: return self.south
            case Mvt.LEFT: return self.west
            case Mvt.RIGHT: return self.east
            case _: return False

def create_cell(x, y, value) -> Cell:
    return Cell(
        x=x,
        y=y,
        north=not bool(value & 1),
        east=not bool(value & 2),
        south=not bool(value & 4),
        west=not bool(value & 8),
    )
