# PACMAN - 42Luxembourg 2026 - kmalfois

from abc import ABC
from math import isclose
from pydantic import BaseModel
from src.data_lib import Movements as Mvt
from src.grid.grid_loader import Grid
from src.grid.cell import Cell


class Token(BaseModel, ABC):
    y: float
    x: float
    speed: float
    current_cell: Cell
    forward_cell: Cell | None = None
    direction: Mvt
    buffered_direction: Mvt | None = None
    active: bool = False

    # Update movement check
    def _update_movements(self, grid: Grid) -> None:
        if self.buffered_direction == self.direction.opposite:
            self.direction = self.direction.opposite
            self._get_forward_cell(grid)
            self.buffered_direction = None
            return
        if self._is_cell_centered() and self.buffered_direction:
                if self._can_move():
                    self.direction = self.buffered_direction
                    self._get_forward_cell(grid)
                    self.buffered_direction = None

    # Recovers forward cell data
    def _get_forward_cell(self, grid: Grid)  -> None:
        y, x = self.current_cell.coordinates
        dir_y, dir_x = self.direction.cell_offset
        self.forward_cell = grid.get_cell(y + dir_y, x + dir_x)

    # [Tool] Return if the entity is allowed to move in current direction
    def _can_move(self) -> bool:
        match self.buffered_direction:
            case Mvt.UP: return self.current_cell.north
            case Mvt.DOWN: return self.current_cell.south
            case Mvt.LEFT: return self.current_cell.west
            case Mvt.RIGHT: return self.current_cell.east
            case _: return False

    # [Tool] Check if entity is at a cell's center
    def _is_cell_centered(self) -> bool:
        cy, cx = self.current_cell.coordinates
        if isclose(self.y, cy + 0.5, abs_tol=0.08) and isclose(self.x, cx + 0.5, abs_tol=0.08):
            return True
        if self.forward_cell:
            fy, fx = self.forward_cell.coordinates
            if isclose(self.y, fy + 0.5, abs_tol=0.08) and isclose(self.x, fx + 0.5, abs_tol=0.08):
                self.current_cell = self.forward_cell
                return True
        return False

    # [Properties]
    @property
    def coordinates(self) -> tuple[float, float]:
        return self.y, self.x

