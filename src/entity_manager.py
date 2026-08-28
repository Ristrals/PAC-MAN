# PACMAN - 42Luxembourg 2026 - kmalfois

from dataclasses import dataclass
from dataclasses import field
from src.config import GameConfig
from src import entity as ent
from src.grid.grid_loader import Grid


@dataclass
class FrameSummary:
    eat_pacgum: bool
    eat_superpacgum: bool
    defeated: bool
    eaten_ghosts: list[ent.Ghost] = field(default_factory=list)


class EntityManager:
    def __init__(self, config: GameConfig) -> None:
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
        self.frame_sumary = FrameSummary()

    def udpate(self) -> FrameSummary:
        # Update ghost target coordinates
        # Check if pacman is centered on a pacgum cell
        # Get pacman powered status
        # Solve collisions
        # return FramSummary report
        pass

    def _gum_check(self) -> None:
        pass

    def _collision_check(self) -> None:
        pass

    def _update_ghosts_target(self) -> None:
