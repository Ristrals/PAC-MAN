# PACMAN - 42Luxembourg 2026 - kmalfois

from abc import ABC, abstractmethod
from math import dist
from pydantic import BaseModel
from src.data_lib import Movements as Mvt
import src.entity as ent
from src.grid.grid_loader import Grid
from src.grid.cell import Cell


# Base ghost behavior class
class GhostBehavior(ABC, BaseModel):
    # Directions in sorted by priority
    _DIRECTION_PRIORITY = [Mvt.UP, Mvt.LEFT, Mvt.DOWN, Mvt.RIGHT]
    ghost: ent.Ghost
    pacman: ent.Pacman
    blinky: ent.Ghost | None = None
    target: tuple[float, float] | None = None

    @abstractmethod
    def get_target(self) -> None:
        """Allow all ghost behaviors to recover their targeted cell"""
        pass

    # Updates buffered direction toward the targeted cell
    def update_direction(
            self, grid: Grid
    ) -> None:
        self.get_target()
        assert isinstance(self.target, tuple)
        self.ghost.target_coord = self.target
        if not self.ghost.direction:
            return
        upcoming_cell = GhostBehavior.get_next_cell(grid, self.ghost.current_cell, self.ghost.direction)
        if not upcoming_cell:
            return
        opposite_dir = self.ghost.direction.opposite if self.ghost.direction else None
        best_dir = self.ghost.direction
        min_dist = float("inf")

        for direction in GhostBehavior._DIRECTION_PRIORITY:
            if direction == opposite_dir:
                continue
            if upcoming_cell.can_exit(direction):
                neighbor_cell = GhostBehavior.get_next_cell(grid, upcoming_cell, direction)
                ny, nx = neighbor_cell.coordinates
                distance = dist((ny + 0.5, nx + 0.5), self.target)
                if distance < min_dist:
                    min_dist = distance
                    best_dir = direction

        self.ghost.buffered_direction = best_dir

    # recover next cell relative to direction
    @classmethod
    def get_next_cell(cls, grid: Grid, current_cell: Cell, direction: Mvt) -> Cell:
        curr_y, curr_x = current_cell.y, current_cell.x
        off_y, off_x = direction.cell_offset
        return grid.get_cell((curr_y + off_y), (curr_x + off_x))
