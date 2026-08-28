# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from math import dist
from src.entity.token import Token
from src import behavior as bhvr


# Ghost states
class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    EATEN = 3


# General Ghost class
class Ghost(Token):
    state: GhostState = GhostState.SCATTER
    target_coord: tuple[float, float] = 0.0, 0.0
    scatter_coord: tuple[float, float] = 0.0, 0.0
    scatter_ai: bhvr.ScatterBehavior = bhvr.ScatterBehavior()
    frighten_ai: bhvr.FrightenBehavior = bhvr.FrightenBehavior()


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
