# PACMAN - 42Luxembourg 2026 - kmalfois

from math import dist
import random
from collections import deque
from enum import Enum
from abc import ABC, abstractmethod
from typing import Callable, Any
from pydantic import ConfigDict, Field, model_validator
from src.data_lib import Movements as Mvt, TextColors as Tc
from src.entity.token import Token
from src.grid.cell import Cell
from src.grid.grid_loader import Grid
import src.entity as ent


class GhostState(Enum):
    """Represent the movement states available to a ghost."""

    CHASE = ("Chase", 0.75, 20.0)
    SCATTER = ("Scatter", 0.75, 5.0)
    FRIGHTENED = ("Frightened", 0.5, 7.0)
    EATEN = ("Eaten", 1.80, 5.0)

    def get_state(self) -> str:
        """Return the display name of the ghost state.

        Returns:
            The human-readable state name.
        """
        return self.value[0]

    def get_speed_ratio(self) -> float:
        """Return the movement speed multiplier for the state.

        Returns:
            The speed ratio associated with the state.
        """
        return self.value[1]


class Ghost(Token, ABC):
    """Base class for ghosts and their state-dependent movement behavior.

    Attributes:
        state: Current state of the ghost.
        target_coord: Coordinates the ghost is currently targeting.
        scatter_coord: Coordinates used as the ghost's scatter target.
        grid: Grid on which the ghost moves.
        pacman: Pac-Man instance targeted by the ghost.
        behaviors: Mapping of states to their behavior methods.
        was_centered: Whether the ghost was centered during the previous update.
        spawn_snapped: Whether an eaten ghost has reached its spawn position.
        respawn_timer: Remaining timer after the ghost reaches its spawn position.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    state: GhostState | None = None
    target_coord: tuple[float, float] = (0.0, 0.0)
    scatter_coord: tuple[float, float] = (0.0, 0.0)
    grid: Grid
    pacman: ent.Pacman
    behaviors: dict[GhostState, Callable[..., Any]] = Field(default_factory=dict, exclude=True)
    was_centered: bool = True  # Required for Ghost direction calculation
    spawn_snapped: bool = False
    respawn_timer: float = 0.0
    _DIRECTION_PRIORITY: list[Mvt] = [Mvt.UP, Mvt.LEFT, Mvt.DOWN, Mvt.RIGHT]

    @model_validator(mode="after")
    def init_sequence(self) -> 'Ghost':
        """Initialize state behaviors and begin ghost movement.

        Returns:
            The initialized ghost.
        """
        self.behaviors = {
            GhostState.CHASE: self._chase_behavior,
            GhostState.SCATTER: self._scatter_behavior,
            GhostState.FRIGHTENED: self._frightened_behavior,
            GhostState.EATEN: self._eaten_behavior,
        }
        self.initiate_movement()
        return self

    def __str__(self) -> str:
        """Return a formatted description of the ghost's current state.

        Returns:
            A string containing the ghost's name, position, target, direction,
            status, and spawn information.
        """
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
                ghost_name = f"{Tc.org}Clyde{Tc.clr}"
        to_print = (
            f"{ghost_name} | "
            f"{Tc.ylw}self{Tc.clr}:({y:.3f},{x:.3f}),{Tc.ylw}tgt{Tc.clr}:({ty:.3f},{tx:.3f}),init:{self.init_coord} | "
            f"{Tc.ylw}dir{Tc.clr}:{self.direction.value if self.direction else None},"
            f"{Tc.ylw}buff_dir{Tc.clr}:{self.buffered_direction.value if self.buffered_direction else None} | "
            f"{Tc.ylw}status{Tc.clr}:{self.state.value[0] if self.state else None} | "
            f"{Tc.ylw}snaped{Tc.clr}:{self.spawn_snapped}"
        )
        if self.state is ent.Gs.EATEN:
            to_print += f" | {Tc.ylw}eaten_timer{Tc.clr}:{self.respawn_timer:.3f}"

        return to_print

    def move(self, delta_time: float, grid: Grid) -> None:
        """Advance the ghost through the grid for one update.

        Args:
            delta_time: Time elapsed since the previous update.
            grid: Grid used to update the ghost's current cell.
        """
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
            self.update_buffered_direction(delta_time)

        # Update center state tracking flag for the next tick
        self.was_centered = currently_centered

    def update_buffered_direction(self, delta_time: float) -> None:
        """Choose the next direction based on the ghost's current state.

        Args:
            delta_time: Time elapsed since the previous update.
        """
        self._get_target()
        if self.state == GhostState.EATEN:
            self._get_bfs_direction(delta_time)
            return
        self._get_proximity_direction()

    # Tracks target via target proximity
    def _get_proximity_direction(self) -> None:
        """Buffer the valid direction closest to the current target."""
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
                neighbor_cell = self._get_next_cell(eval_cell, direction)
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

    # Directly traces the shortest path to the target
    def _get_bfs_direction(self, delta_time: float) -> None:
        """Buffer the first direction on a shortest path to the target.

        Args:
            delta_time: Time elapsed since the previous update.
        """
        if self.spawn_snapped:
            self.direction = None
            self.buffered_direction = None
            return

        if self._check_eaten_arrival(delta_time):
            return

        if not self.direction:
            for move in self._DIRECTION_PRIORITY:
                if self.current_cell.can_exit(move):
                    self.direction = move
                    break

        start_coords: tuple[int, int] = self.current_cell.coordinates
        target_coords: tuple[int, int] = (int(self.target_coord[0]), int(self.target_coord[1]))

        queue: deque[tuple[Cell, Mvt]] = deque()
        visited = {start_coords}

        for direction in self._DIRECTION_PRIORITY:
            if self.current_cell.can_exit(direction):
                neighbor = self._get_next_cell(self.current_cell, direction)
                if neighbor:
                    n_coords = neighbor.coordinates
                    if n_coords not in visited:
                        if n_coords == target_coords:
                            self.buffered_direction = direction
                            return
                        visited.add(n_coords)
                        queue.append((neighbor, direction))

        while queue:
            curr_cell, initial_direction = queue.popleft()
            for direction in self._DIRECTION_PRIORITY:
                if curr_cell.can_exit(direction):
                    neighbor = self._get_next_cell(curr_cell, direction)
                    if neighbor:
                        n_coords = neighbor.coordinates
                        if n_coords not in visited:
                            if n_coords == target_coords:
                                self.buffered_direction = initial_direction
                                return
                            visited.add(n_coords)
                            queue.append((neighbor, initial_direction))

        self.buffered_direction = self.direction

    # Recovers next cell on trajectory
    def _get_next_cell(self, current_cell: Cell, direction: Mvt) -> Cell | None:
        """Return the neighboring cell in a direction when it is in bounds.

        Args:
            current_cell: Cell from which to move.
            direction: Direction of the neighboring cell.

        Returns:
            The neighboring cell, or ``None`` when the position is out of bounds.
        """
        curr_y, curr_x = current_cell.y, current_cell.x
        off_y, off_x = direction.cell_offset
        ny, nx = curr_y + off_y, curr_x + off_x
        if 0 <= ny < self.grid.height and 0 <= nx < self.grid.width:
            return self.grid.get_cell(ny, nx)
        return None

    # Recovers target tile relative to current state
    def _get_target(self) -> None:
        """Update the target coordinates using the current ghost behavior."""
        if self.state and self.state in self.behaviors:
            self.behaviors[self.state]()

    # Checks if ghost are back on their spawn tile while eaten
    def _check_eaten_arrival(self, delta_time: float) -> bool:
        """Check whether an eaten ghost has reached its initial position.

        Args:
            delta_time: Time elapsed since the previous update.

        Returns:
            Whether the ghost arrived at its spawn position during the update.
        """
        assert isinstance(self.init_coord, tuple)
        target_y, target_x = self.init_coord
        dist_y = abs(self.y - target_y)
        dist_x = abs(self.x - target_x)

        step_distance = self.speed * delta_time
        tolerance = max(0.08, step_distance * 0.75)

        if dist_y <= tolerance and dist_x <= tolerance:
            # print(f"<<<<< {self.__class__.__name__} - ARRIVED >>>>>")  # test print
            self.y, self.x = self.current_cell.center_coord
            self.direction = None
            self.buffered_direction = None
            self.respawn_timer = GhostState.EATEN.value[2]
            self.spawn_snapped = True
            return True
        return False

    def _get_relative_distance(self, target: tuple[float, float]) -> float:
        """Return the Euclidean distance from the ghost to a target.

        Args:
            target: Coordinates of the target position.

        Returns:
            The distance between the ghost and the target.
        """
        return dist(self.coordinates, target)

    # [Behaviors]
    @abstractmethod
    def _chase_behavior(self) -> None:
        """Set the target coordinates for the concrete ghost's chase mode."""
        pass

    def _scatter_behavior(self) -> None:
        """Set the scatter position as the ghost's current target."""
        self.target_coord = self.scatter_coord

    def _frightened_behavior(self) -> None:
        """Leave targeting unused because frightened movement is random."""
        pass

    def _eaten_behavior(self) -> None:
        """Set the initial position as the target while the ghost is eaten."""
        if self.init_coord:
            self.target_coord = self.init_coord

    # [Tools]
    @staticmethod
    def to_grid_position(coordinates: tuple[float, float]) -> tuple[int, int]:
        """Convert floating-point coordinates to an integer grid position.

        Args:
            coordinates: Coordinates in ``(y, x)`` order.

        Returns:
            The integer position in ``(x, y)`` order.
        """
        y, x = coordinates
        return int(x), int(y)

    def initiate_movement(self) -> None:
        """Set the first available direction according to priority order."""
        for direction in self._DIRECTION_PRIORITY:
            if self.can_move(direction):
                self.direction = direction
                break
