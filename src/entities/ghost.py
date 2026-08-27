# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from src.entities.token import Token
from src import behavior as bhvr


class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    EATEN = 3

class Ghost(Token):
    state: GhostState = GhostState.SCATTER
    target_y: float = 0.0
    target_x: float = 0.0
    scatter_y: float = 0.0
    scatter_x: float = 0.0
    scatter_ai: bhvr.ScatterBehavior = bhvr.ScatterBehavior()
    frighten_ai: bhvr.FrightenBehavior = bhvr.FrightenBehavior()

    def _get_pacman(self, pacman_position: tuple[float, float]) -> None:
        self.target_y, self.target_x = pacman_position


# Red ghost
class Blinky(Ghost):
    ghost_ai: bhvr.BlinkyBehavior = bhvr.BlinkyBehavior()
    pass


# Pink ghost
class Pinky(Ghost):
    ghost_ai: bhvr.PinkyBehavior = bhvr.PinkyBehavior()
    pass


# Cyan ghost
class Inky(Ghost):
    ghost_ai: bhvr.InkyBehavior = bhvr.InkyBehavior()
    pass


# Orange ghost
class Clyde(Ghost):
    ghost_ai: bhvr.ClydeBehavior = bhvr.ClydeBehavior()
    pass

