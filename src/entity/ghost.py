# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from math import dist
import random
from abc import ABC, abstractmethod
from typing import Callable, Any
from pydantic import ConfigDict, Field, model_validator
from src.data_lib import Movements as Mvt, TextColors as Tc
from src.entity.token import Token
from src.grid.cell import Cell
from src.grid.grid_loader import Grid
import src.entity as ent


class GhostState(Enum):
    CHASE = ("Chase", 0.75, 20.0)
    SCATTER = ("Scatter", 0.75, 5.0)
    FRIGHTENED = ("Frightened", 0.5, 7.0)
    EATEN = ("Eaten", 1.80, 7.0)

    def get_state(self) -> str:
        return self.value[0]

    def get_speed_ratio(self) -> float:
        return self.value[1]


class Ghost(Token, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    state: GhostState | None = None
    target_coord: tuple[float, float] = (0.0, 0.0)
    scatter_coord: tuple[float, float] = (0.0, 0.0)
    grid: Grid
    pacman: ent.Pacman
    behaviors: dict[GhostState, Callable[..., Any]] = Field(default_factory=dict, exclude=True)
    was_centered: bool = True  # Required for Ghost direction calculation
    eaten_timer: float = 0.0
    _DIRECTION_PRIORITY: list[Mvt] = [Mvt.UP, Mvt.LEFT, Mvt.DOWN, Mvt.RIGHT]

    @model_validator(mode="after")
    def init_sequence(self) -> 'Ghost':
        self.behaviors = {
            GhostState.CHASE: self._chase_behavior,
            GhostState.SCATTER: self._scatter_behavior,
            GhostState.FRIGHTENED: self._frightened_behavior,
            GhostState.EATEN: self._eaten_behavior,
        }
        for move in self._DIRECTION_PRIORITY:
            if self.can_move(move):
                self.direction = move
                continue
        return self

    def __str__(self) -> str:
        ghost_name = ""
        y, x = self.coordinates
        ty, tx = self.target_coord
        match self.__class__.__name__:
            case "Blinky":
                ghost_name = f"{Tc.red}Blinky{Tc.clr}"
            case "Pinky":
                ghost_name = f"{Tc.pnk}Pinky{Tc.clr}"
            case "Inky":
                ghost_name = f"{Tc.cyn}Inky{Tc.clr}"
            case "Clyde":
                ghost_name = f"{Tc.org}Inky{Tc.clr}"
        to_print = (
            f"{ghost_name} | "
            f"{Tc.ylw}self{Tc.clr}:({y:.3f},{x:.3f}),{Tc.ylw}tgt{Tc.clr}:({ty:.3f},{tx:.3f}) | "
            f"{Tc.ylw}dir{Tc.clr}:{self.direction.value if self.direction else None},"
            f"{Tc.ylw}buff_dir{Tc.clr}:{self.buffered_direction.value if self.buffered_direction else None} | "
            f"{self.state.value[0] if self.state else None}"
        )
        if self.state is ent.Gs.EATEN:
            to_print += f" | {Tc.ylw}eaten_timer{Tc.clr}:{self.eaten_timer:.3f}"

        return to_print

    def move(self, delta_time: float, grid: Grid) -> None:
        if not self.active:
            return

        currently_centered = self.is_cell_centered()

        if currently_centered and not self.was_centered:
            cy, cx = self.current_cell.coordinates

            if self.buffered_direction and self.current_cell.can_exit(self.buffered_direction):
                self.direction = self.buffered_direction

                if self.direction in (Mvt.UP, Mvt.DOWN):
                    self.x = cx + 0.5
                else:
                    self.y = cy + 0.5

                self.buffered_direction = None

        if self.direction is not None and (self.current_cell.can_exit(self.direction) or not currently_centered):
            speed_ratio = self.state.get_speed_ratio() if self.state else 1.0
            effective_speed = self.speed * speed_ratio

            dir_y, dir_x = self.direction.cell_offset
            self.y += dir_y * effective_speed * delta_time
            self.x += dir_x * effective_speed * delta_time

            # Update current cell reference if crossed tile boundary
            new_cy, new_cx = int(self.y), int(self.x)
            if (new_cy, new_cx) != self.current_cell.coordinates:
                self.current_cell = grid.get_cell(new_cy, new_cx)

        if self.was_centered and not currently_centered:
            self.update_buffered_direction()

        # Update center state tracking flag for the next tick
        self.was_centered = currently_centered

    def update_buffered_direction(self) -> None:
        self._get_target()
        if not self.direction:
            return

        # Evaluate directions from the CURRENT cell the ghost is occupying
        eval_cell = self.current_cell
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

        if not valid_directions:
            if eval_cell.can_exit(opposite_dir):
                self.buffered_direction = opposite_dir
            return

        if self.state == GhostState.FRIGHTENED:
            if valid_directions:
                self.buffered_direction = random.choice(valid_directions)
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
