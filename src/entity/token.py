# PACMAN - 42Luxembourg 2026 - kmalfois

from abc import ABC
from math import isclose
from pydantic import BaseModel, model_validator
from src.data_lib import Movements as Mvt
from src.grid.grid_loader import Grid
from src.grid.cell import Cell


class Token(BaseModel, ABC):
    y: float = 0.0
    x: float = 0.0
    speed: float = 0.0
    current_cell: Cell
    direction: Mvt | None = None
    buffered_direction: Mvt | None = None
    active: bool = False

    # Initial position in case of reset
    init_coord: tuple[float, float] | None = None
    init_cell: Cell | None = None

    # Sets initial position after item creation
    @model_validator(mode="after")
    def _set_initial_position(self) -> 'Token':
        if self.init_coord is None:
            self.init_cood = (self.y, self.x)
        if self.init_cell is None:
            self.init_cell = self.current_cell
        return self

    # Reset token to initial position
    def reset_position(self) -> None:
        assert (
            isinstance(self.init_cell, Cell) and
            isinstance(self.init_coord, tuple)
        )
        self.y, self.x = self.init_coord
        self.current_cell = self.init_cell

    # Movement
    def move(self, delta_time: float, grid: Grid) -> None:
        if not self.active:
            return

        cy, cx = self.current_cell.coordinates
        at_center = self.is_cell_centered()

        if self.buffered_direction:
            if self.direction is None or self.buffered_direction == self.direction.opposite:
                if self._can_move(self.buffered_direction):
                    self.direction = self.buffered_direction
                    self.buffered_direction = None
            elif at_center and self._can_move(self.buffered_direction):
                self.direction = self.buffered_direction
                self.y, self.x = cy + 0.5, cx + 0.5
                self.buffered_direction = None

        if self.direction is None:
            return

        if not self._can_move(self.direction) and at_center:
            self.y, self.x = cy + 0.5, cx + 0.5
            return

        dir_y, dir_x = self.direction.cell_offset
        self.y += dir_y * self.speed * delta_time
        self.x += dir_x * self.speed * delta_time

        new_cy, new_cx = int(self.y), int(self.x)
        if (new_cy, new_cx) != (cy, cx):
            self.current_cell = grid.get_cell(new_cy, new_cx)

    # Check if token is at cell center
    def is_cell_centered(self) -> bool:
        cy, cx = self.current_cell.coordinates
        if isclose(self.y, cy + 0.5, abs_tol=0.08) and isclose(self.x, cx + 0.5, abs_tol=0.08):
            return True
        return False

    # Return if the entity is allowed to move in current direction
    def _can_move(self, direction: Mvt | None) -> bool:
        match direction:
            case Mvt.UP: return self.current_cell.north
            case Mvt.DOWN: return self.current_cell.south
            case Mvt.LEFT: return self.current_cell.west
            case Mvt.RIGHT: return self.current_cell.east
            case _: return False


    # [Properties]
    @property
    def coordinates(self) -> tuple[float, float]:
        return self.y, self.x

    @coordinates.setter
    def coordinates(self, value: tuple[float, float] | None) -> None:
        assert isinstance(value, tuple)
        self.y, self.x = value

    @property
    def current_direction(self) -> Mvt | None:
        return self.direction

    @property
    def input_direction(self) -> Mvt | None:
        return self.buffered_direction

    @input_direction.setter
    def input_direction(self, value: Mvt | None) -> None:
        self.buffered_direction = value
