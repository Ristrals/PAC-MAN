# PACMAN - 42Luxembourg 2026 - kmalfois

from typing import Annotated
from abc import ABC
from pydantic import BaseModel, Field
from src.data_lib import Movements as Mvt, Movements
from src.grid.grid_loader import Grid
from src.grid.cell import Cell


class Token(BaseModel, ABC):
    _y: Annotated[float, Field(alias="y", description="Coordinate y")]
    _x: Annotated[float, Field(alias="x", description="Coordinate x")]
    _speed: Annotated[float, Field(alias="speed", description="Token's speed")]
    _cell: Annotated[Cell, Field(alias="cell", description="Currently assigned Cell")]
    _toward_cell: Annotated[Cell | None, Field(alias="cell", description="Cell moved toward")]
    _direction: Annotated[Mvt, Field(alias="direction", description="current direction")]
    _buffered_direction: Annotated[Mvt, Field(alias="buffered_direction", description="current direction")]
    _active: Annotated[bool, Field(alias="active", description="Is this entity active?")]

    def _can_move(self, movement: Movements, grid: Grid) -> bool:
        current_cell: Cell = grid.get_cell( self._y, self._x)
        if not current_cell:
            return False
        if current_cell.north and movement == Mvt.UP:
            return False
        if current_cell.south and movement == Mvt.DOWN:
            return False
        if current_cell.east and movement == Mvt.RIGHT:
            return False
        if current_cell.west and movement == Mvt.LEFT:
            return False
        return True

    def _get_toward_cell(self, grid: Grid)  -> None:
        
        if self._direction == Mvt.UP:
            self._toward_cell = self._cell
        pass

    def _update_authorized_movements(self, cell: Cell):


    def move(self, movement: Mvt, grid: Grid) -> None:
        if self._can_move(movement):


