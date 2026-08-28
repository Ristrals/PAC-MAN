# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from math import isclose
from src.entity.token import Token
from src import behavior as bhvr


class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    EATEN = 3

class Ghost(Token):
    state: GhostState = GhostState.SCATTER
    target_coord: tuple[float, float] = 0.0, 0.0
    scatter_coord: tuple[float, float] = 0.0, 0.0
    scatter_ai: bhvr.ScatterBehavior = bhvr.ScatterBehavior()
    frighten_ai: bhvr.FrightenBehavior = bhvr.FrightenBehavior()

    def collision_check(self, coordinates: tuple[float, float]) -> bool:
        py, px = coordinates
        if isclose(self.y, py, abs_tol=0.08) and isclose(self.x, px, abs_tol=0.08):
            return True
        return False


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

