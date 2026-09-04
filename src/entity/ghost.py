# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from math import dist
import random
from abc import ABC, abstractmethod
from typing import Callable, Any
from pydantic import ConfigDict, Field, model_validator
from src.data_lib import Movements as Mvt
from src.entity.token import Token
from src.grid.cell import Cell
from src.grid.grid_loader import Grid
import src.entity as ent


class GhostState(Enum):
    CHASE = ("chase", 0.75)
    SCATTER = ("scatter", 0.75)
    FRIGHTENED = ("frightened", 0.5)
    EATEN = ("eaten", 1.80)

    def get_state(self) -> str:
        return self.value[0]

    def get_speed_ratio(self) -> float:
        return self.value[1]


class Ghost(Token, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    state: GhostState | None = GhostState.SCATTER
    target_coord: tuple[float, float] = (0.0, 0.0)
    scatter_coord: tuple[float, float] = (0.0, 0.0)
    grid: Grid
    pacman: ent.Pacman
    behaviors: dict[GhostState, Callable[..., Any]] = Field(default_factory=dict, exclude=True)
    _DIRECTION_PRIORITY: list[Mvt] = [Mvt.UP, Mvt.LEFT, Mvt.DOWN, Mvt.RIGHT]

    @model_validator(mode="after")
    def init_sequence(self) -> 'Ghost':
        self.behaviors = {
            GhostState.CHASE: self._chase_behavior,
            GhostState.SCATTER: self._scatter_behavior,
            GhostState.FRIGHTENED: self._frightened_behavior,
            GhostState.EATEN: self._eaten_behavior,
        }
        return self

    def update_buffered_direction(self) -> None:
        self._get_target()
        if not self.direction:
            return

        upcoming_cell = Ghost._get_next_cell(self.grid, self.current_cell, self.direction)

        if not upcoming_cell or not self.current_cell.can_exit(self.direction):
            eval_cell = self.current_cell
        else:
            eval_cell = upcoming_cell

        opposite_dir = self.direction.opposite
        best_dir: Mvt | None = None
        min_dist = float("inf")
        valid_directions: list[Mvt] = []

        for direction in self._DIRECTION_PRIORITY:
            if direction == opposite_dir:
                continue

            if eval_cell.can_exit(direction):
                neighbor_cell = Ghost._get_next_cell(self.grid, eval_cell, direction)
                if not neighbor_cell:
                    continue

                valid_directions.append(direction)
                ny, nx = neighbor_cell.coordinates
                distance = dist((ny + 0.5, nx + 0.5), self.target_coord)
                if distance < min_dist:
                    min_dist = distance
                    best_dir = direction

        if self.state == GhostState.FRIGHTENED:
            self.buffered_direction = random.choice(valid_directions) if valid_directions else opposite_dir
            return

        if best_dir is not None:
            self.buffered_direction = best_dir
        elif valid_directions:
            self.buffered_direction = valid_directions[0]

    @classmethod
    def _get_next_cell(cls, grid: Grid, current_cell: Cell, direction: Mvt) -> Cell | None:
        curr_y, curr_x = current_cell.y, current_cell.x
        off_y, off_x = direction.cell_offset
        ny, nx = curr_y + off_y, curr_x + off_x
        if 0 <= ny < grid.height and 0 <= nx < grid.width:
            return grid.get_cell(ny, nx)
        return None

    def _get_target(self) -> None:
        if self.state and self.state in self.behaviors:
            self.behaviors[self.state]()

    @abstractmethod
    def _chase_behavior(self) -> None:
        """Specific ghost behaviors to recover their targeted cell"""
        pass

    def _scatter_behavior(self) -> None:
        self.target_coord = self.scatter_coord

    def _frightened_behavior(self) -> None:
        """Target coordinate unused; movement selected pseudo-randomly."""
        pass

    def _eaten_behavior(self) -> None:
        self.target_coord = self.scatter_coord