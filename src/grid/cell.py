from dataclasses import dataclass
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


def create_cell(x, y, value) -> Cell:
    return Cell(
        x=x,
        y=y,
        north=not bool(value & 1),
        east=not bool(value & 2),
        south=not bool(value & 4),
        west=not bool(value & 8),
    )
