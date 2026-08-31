# PACMAN - 42Luxembourg 2026 - kmalfois

from dataclasses import dataclass, field
from math import dist
from src import entity as ent
from src.grid.grid_loader import Grid
from src.grid.cell import StateType as St, Cell


@dataclass
class FrameSummary:
    eat_pacgum: bool = False
    eat_superpacgum: bool = False
    defeated: bool = False
    eaten_ghosts: list[ent.Ghost] = field(default_factory=list)


# TO DO:
class EntityManager:
    def __init__(self, grid: Grid, base_speed: float = 3.0) -> None:
        self.grid: Grid = grid
        self.base_speed: float = base_speed
        self._place_tokens()

    def update(self, delta_time: float) -> FrameSummary:
        summary = FrameSummary()

        # All token move
        self.pacman.move(delta_time, self.grid)
        for ghost in self.ghosts:
            ghost.move(delta_time, self.grid)

        # Check if pacman is centered on a pacgum cell
        if self.pacman.is_cell_centered():
            match self.pacman.current_cell.state_type:
                case St.PACGUM:
                    summary.eat_pacgum = True
                    self.pacman.current_cell.state_type = St.EMPTY
                case St.SUPER_PACGUM:
                    summary.eat_superpacgum = True
                    for ghost in self.ghosts:
                        if ghost.state != ent.Gs.EATEN:
                            ghost.state = ent.Gs.FRIGHTENED
                    self.pacman.current_cell.state_type = St.EMPTY

        # Solve collisions
        for ghost in self.ghosts:
            if dist(ghost.coordinates, self.pacman.coordinates) < 0.5:
                match ghost.state:
                    case ent.Gs.FRIGHTENED:
                        summary.eaten_ghosts.append(ghost)
                        ghost.state = ent.Gs.EATEN
                    case ent.Gs.CHASE | ent.Gs.SCATTER:
                        summary.defeated = True
                        self.pacman.active = False
                        break

        # Update ghost target coordinates
        for ghost in self.ghosts:
            if not self.pacman.active:  # if pacman was defeated all ghosts turn inactive
                ghost.active = False
            ghost.target_coord = self.pacman.coordinates

        # return FrameSummary report
        return summary

    # Resets all token positions
    def reset_positions(self) -> None:
        self.pacman.coordinates = self.pacman.init_coord
        for ghost in self.ghosts:
            ghost.coordinates = ghost.init_coord

    # Adjust all ghost speeds
    def set_ghost_speeds(self, speed: float) -> None:
        for ghost in self.ghosts:
            if ghost.state != ent.Gs.EATEN:
                ghost.speed = speed * self.base_speed

    # Adjust all ghost states
    def set_ghost_states(self, ghost_state: ent.Gs) -> None:
        for ghost in self.ghosts:
            if ghost.state != ent.Gs.EATEN:
                ghost.state = ghost_state

    def _place_tokens(self) -> None:
        pacman_pos: Cell = self.grid.get_cell(self.grid.height//2, self.grid.width//2)
        ghosts_pos: list[Cell] = [
            self.grid.get_cell(0, 0),
            self.grid.get_cell(0, self.grid.width - 1),
            self.grid.get_cell(self.grid.width - 1, self.grid.height - 1),
            self.grid.get_cell(self.grid.height - 1, 0)
        ]

        self.pacman: ent.Pacman = ent.Pacman(y=pacman_pos.y + 0.5, x=pacman_pos.x + 0.5,
                                             current_cell=pacman_pos, speed=(0.80 * self.base_speed))
        self.ghosts: list[ent.Ghost] = [
            ent.Blinky(y=ghosts_pos[0].y + 0.5, x=ghosts_pos[0].x + 0.5, current_cell=ghosts_pos[0],
                       target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[0].y, ghosts_pos[0].x)),
            ent.Pinky(y=ghosts_pos[1].y + 0.5, x=ghosts_pos[1].x + 0.5, current_cell=ghosts_pos[1],
                      target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[1].y, ghosts_pos[1].x)),
            ent.Inky(y=ghosts_pos[2].y + 0.5, x=ghosts_pos[2].x + 0.5, current_cell=ghosts_pos[2],
                     target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[2].y, ghosts_pos[2].x)),
            ent.Clyde(y=ghosts_pos[3].y + 0.5, x=ghosts_pos[3].x + 0.5, current_cell=ghosts_pos[3],
                      target_coord=self.pacman.coordinates, scatter_coord=(ghosts_pos[3].y, ghosts_pos[3].x)),
        ]
