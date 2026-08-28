# PACMAN - 42Luxembourg 2026 - kmalfois

from dataclasses import dataclass, field
from math import dist
from src import entity as ent
from src.config import GameConfig
from src.grid.grid_loader import Grid
from src.grid.cell import StateType as St


@dataclass
class FrameSummary:
    eat_pacgum: bool = False
    eat_superpacgum: bool = False
    defeated: bool = False
    eaten_ghosts: list[ent.Ghost] = field(default_factory=list)


class EntityManager:
    def __init__(self, config: GameConfig, grid: Grid) -> None:
        self.config: GameConfig = config
        self.grid: Grid = grid
        self.pacman: ent.Pacman = ent.Pacman(y=,x=,current_cell=,speed=)
        self.ghosts: list[ent.Ghost] = [
            ent.Blinky(y=, x=, current_cell=, speed=,
                       target_coord=self.pacman.coordinates, scatter_coord=),
            ent.Pinky(y=, x=, current_cell=, speed=,
                      target_coord=self.pacman.coordinates, scatter_coord=),
            ent.Inky(y=, x=, current_cell=, speed=,
                     target_coord=self.pacman.coordinates, scatter_coord=),
            ent.Clyde(y=, x=, current_cell=, speed=,
                      target_coord=self.pacman.coordinates, scatter_coord=),
        ]

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
                    case ent.Gs.CHASE, ent.Gs.SCATTER:
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
    def set_ghost_speeds(self, speed: float) ->None:
        for ghost in self.ghosts:
            if ghost.state != ent.Gs.EATEN:
                ghost.speed = speed

    # Adjust all ghost states
    def set_ghost_states(self, ghost_state: ent.Gs) -> None:
        for ghost in self.ghosts:
            if ghost.state != ent.Gs.EATEN:
                ghost.state = ghost_state