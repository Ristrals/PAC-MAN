# PACMAN - 42Luxembourg 2026 - kmalfois

from dataclasses import dataclass, field
from math import dist
import src.entity as ent
from src.grid.grid_loader import Grid
from src.grid.cell import StateType as St, Cell
from src.data_lib import Movements as Mvt


@dataclass
class FrameSummary:
    eat_pacgum: bool = False
    eat_superpacgum: bool = False
    defeated: bool = False
    eaten_ghosts: list[ent.Ghost] = field(default_factory=list)


class EntityManager:
    def __init__(self, grid: Grid, base_speed: float = 3.0) -> None:
        self.grid: Grid = grid
        self.base_speed: float = base_speed

        # Game timer attributes
        self._timer: float = 0.0
        self.frighten_timer: float = 0.0
        self.current_behavior: ent.Gs = ent.Gs.CHASE
        self._base_behavior: ent.Gs = ent.Gs.CHASE
        self.ghost_freeze: bool = False
        self._initialize_tokens()

    def update(self, delta_time: float) -> FrameSummary:
        summary = FrameSummary()

        self._update_ghost_states(delta_time)

        # All token move
        self.pacman.move(delta_time, self.grid)
        # print(self.pacman)
        if not self.ghost_freeze:
            for ghost in self.ghosts:
                # print(ghost)
                ghost.update_buffered_direction(delta_time)
                ghost.move(delta_time, self.grid)

        # Check if pacman is centered on a pacgum cell
        match self.pacman.current_cell.state_type:
            case St.PACGUM:
                summary.eat_pacgum = True
                self.pacman.current_cell.state_type = St.EMPTY
            case St.SUPER_PACGUM:
                summary.eat_superpacgum = True
                self.set_ghost_states(ent.Gs.FRIGHTENED)
                self.pacman.current_cell.state_type = St.EMPTY

        # Solve collisions
        if not self.pacman.is_invincible:
            for ghost in self.ghosts:
                if dist(ghost.coordinates, self.pacman.coordinates) < 0.5:
                    match ghost.state:
                        case ent.Gs.FRIGHTENED:
                            summary.eaten_ghosts.append(ghost)
                            ghost.respawn_timer = ent.Gs.EATEN.value[2]
                            ghost.state = ent.Gs.EATEN
                        case ent.Gs.CHASE | ent.Gs.SCATTER:
                            summary.defeated = True
                            self.pacman.active = False
                            break

        # return FrameSummary report
        return summary

    # Resets all token positions
    def reset_positions(self) -> None:
        self.pacman.coordinates = self.pacman.init_coord
        assert isinstance(self.pacman.init_coord, tuple)
        py, px = self.pacman.init_coord
        self.pacman.current_cell = self.grid.get_cell(int(py), int(px))
        for ghost in self.ghosts:
            ghost.direction = None
            ghost.buffered_direction = None
            ghost.respawn_timer = 0.0
            ghost.state = self._base_behavior
            ghost.coordinates = ghost.init_coord
            assert isinstance(ghost.init_coord, tuple)
            gy, gx = ghost.init_coord
            ghost.current_cell = self.grid.get_cell(int(gy), int(gx))
            ghost.initiate_movement()


    # Update Ghost behaviors regarding Delta Time
    def _update_ghost_states(self, delta_time: float) -> None:
        for ghost in self.ghosts:
            if ghost.state == ent.Gs.EATEN and ghost.spawn_snapped:
                ghost.respawn_timer -= delta_time
                if ghost.respawn_timer <= 0.0:
                    self._respawn_ghost(ghost)

        if self.current_behavior == ent.Gs.FRIGHTENED:
            self.frighten_timer -= delta_time
            if self.frighten_timer <= 0.0:
                self.set_ghost_states(self._base_behavior)
            return

        self._timer -= delta_time
        if self._timer <= 0.0:
            match self.current_behavior:
                case ent.Gs.CHASE:
                    self._base_behavior = ent.Gs.SCATTER
                    self.set_ghost_states(ent.Gs.SCATTER)
                case ent.Gs.SCATTER:
                    self._base_behavior = ent.Gs.CHASE
                    self.set_ghost_states(ent.Gs.CHASE)

    # Adjust all ghost states and speed
    def set_ghost_states(self, ghost_state: ent.Gs) -> None:
        match ghost_state:
            case (ent.Gs.CHASE | ent.Gs.SCATTER):
                if self.current_behavior != ent.Gs.FRIGHTENED:
                    self._timer = ghost_state.value[2]
            case ent.Gs.FRIGHTENED:
                self.frighten_timer = ghost_state.value[2]
        self.current_behavior = ghost_state
        for ghost in self.ghosts:
            if ghost.state != ent.Gs.EATEN:
                ghost.state = ghost_state
                if ghost_state == ent.Gs.FRIGHTENED and ghost.direction:
                    if ghost.current_cell.can_exit(ghost.direction.opposite):
                        ghost.direction = ghost.direction.opposite
                    else:
                        if ghost.is_cell_centered():
                            ghost.initiate_movement()
                ghost.speed = ghost_state.get_speed_ratio() * self.base_speed

    # Initializes all tokens
    def _initialize_tokens(self) -> None:
        pacman_pos: Cell = self.grid.get_center_position()
        ghosts_pos: list[Cell] = [
            self.grid.get_cell(0, 1),  # Blinky
            self.grid.get_cell(1, self.grid.width),  # Pinky
            self.grid.get_cell(self.grid.height, self.grid.width - 2),  # Inky
            self.grid.get_cell((self.grid.height - 2), 0)  # Clyde
        ]

        # Placing Pacman
        self.pacman: ent.Pacman = ent.Pacman(y=pacman_pos.y + 0.5, x=pacman_pos.x + 0.5,
                                             current_cell=pacman_pos, speed=(0.80 * self.base_speed))

        # Placing and setting ghosts to Scatter mode
        blinky = ent.Blinky(
            y=ghosts_pos[0].y + 0.5, x=ghosts_pos[0].x + 0.5, current_cell=ghosts_pos[0], grid=self.grid,
            target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[0].y + 0.5, ghosts_pos[0].x + 0.5),
            pacman=self.pacman)
        pinky = ent.Pinky(
            y=ghosts_pos[1].y + 0.5, x=ghosts_pos[1].x + 0.5, current_cell=ghosts_pos[1], grid=self.grid,
            target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[1].y + 0.5, ghosts_pos[1].x + 0.5),
            pacman=self.pacman)
        inky = ent.Inky(
            y=ghosts_pos[2].y + 0.5, x=ghosts_pos[2].x + 0.5, current_cell=ghosts_pos[2], grid=self.grid,
            target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[2].y + 0.5, ghosts_pos[2].x + 0.5),
            pacman=self.pacman, blinky=blinky)
        clyde = ent.Clyde(
            y=ghosts_pos[3].y + 0.5, x=ghosts_pos[3].x + 0.5, current_cell=ghosts_pos[3], grid=self.grid,
            target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[3].y + 0.5, ghosts_pos[3].x + 0.5),
            pacman=self.pacman)
        self.ghosts: tuple[ent.Blinky, ent.Pinky, ent.Inky, ent.Clyde] = (blinky, pinky, inky, clyde)
        self.set_ghost_states(ent.Gs.SCATTER)

    def _respawn_ghost(self, ghost: ent.Ghost) -> None:
        ghost.respawn_timer = 0.0
        ghost.state = self._base_behavior
        ghost.speed = self._base_behavior.value[1] * self.base_speed
        ghost.spawn_snapped = False
        ghost.initiate_movement()
