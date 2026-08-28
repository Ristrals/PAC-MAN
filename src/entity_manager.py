# PACMAN - 42Luxembourg 2026 - kmalfois

from dataclasses import dataclass
from dataclasses import field
from src import entity as ent
from src.config import GameConfig
from src.grid.grid_loader import Grid
from src.grid.cell import StateType as St


@dataclass
class FrameSummary:
    eat_pacgum: bool
    eat_superpacgum: bool
    defeated: bool
    eaten_ghosts: list[ent.Ghost] = field(default_factory=list)


class EntityManager:
    def __init__(self, config: GameConfig) -> None:
        self.config: GameConfig = config
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

    def udpate(self, delta_time: float, grid: Grid) -> FrameSummary:
        score_delta: int = 0
        pacman_defeated: bool = False
        eaten_ghosts: list[ent.Ghost] = []

        # All move
        self.pacman.move(delta_time, grid)
        for ghost in self.ghosts:
            ghost.move(delta_time, grid)

        # Check if pacman is centered on a pacgum cell
        if self.pacman.is_cell_centered():
            match self.pacman.current_cell.state_type:
                case St.PACGUM:
                    score_delta += self.config.points_per_pacgum
                    self.pacman.current_cell.state_type = St.EMPTY
                case St.SUPER_PACGUM:
                    score_delta += self.config.points_per_super_pacgum
                    self.pacman.current_cell.state_type = St.EMPTY
        
        # Solve collisions

        # Update ghost target coordinates
        # return FramSummary report
        return self.frame_sumary

    def _gum_check(self) -> None:
        pass

    def _collision_check(self) -> None:
        pass

    def _update_ghosts_target(self) -> None:
        pass

# # src/game.py
#
# class EntityManager:
#     """Handles token movement and interaction detection."""
#
#     def __init__(self, grid: Grid):
#         self.grid = grid
#         self.pacman = Pacman(...)
#         self.ghosts: list[Ghost] = [Blinky(...), Pinky(...), Inky(...), Clyde(...)]
#
#     def update(self, dt: float) -> tuple[int, bool, Ghost | None]:
#         """
#         Updates physics & interactions.
#         Returns a tuple of results back to GameController:
#         (score_delta, pacman_died_flag, ghost_eaten_obj)
#         """
#         score_delta = 0
#         pacman_died = False
#         eaten_ghost = None
#
#         # 1. Physics updates
#         self.pacman.move(dt, self.grid)
#         for ghost in self.ghosts:
#             ghost.move(dt, self.grid)
#
#         # 2. Check Pellets
#         if self.pacman._is_cell_centered():
#             cell = self.pacman.current_cell
#             if cell.state_type == St.PACGUM:
#                 cell.state_type = St.EMPTY
#                 score_delta += 10
#             elif cell.state_type == St.SUPER_PACGUM:
#                 cell.state_type = St.EMPTY
#                 score_delta += 50
#                 self._trigger_frightened_ghosts()
#
#         # 3. Check Ghost Collisions
#         for ghost in self.ghosts:
#             if math.dist(self.pacman.coordinates, ghost.coordinates) < 0.5:
#                 if ghost.state == GhostState.FRIGHTENED:
#                     eaten_ghost = ghost
#                 elif ghost.state in (GhostState.CHASE, GhostState.SCATTER):
#                     pacman_died = True
#
#         return score_delta, pacman_died, eaten_ghost