# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from src.entity.token import Token
from src import behavior as bhvr
from pydantic import ConfigDict


# Ghost states
class GhostState(Enum):
    CHASE = ("chase", 0.75, None)
    SCATTER = ("scatter", 0.75, bhvr.ScatterBehavior())
    FRIGHTENED = ("frightened", 0.5, bhvr.FrightenBehavior())
    EATEN = ("eaten", 1.80, bhvr.EatenBehavior())

    def get_state(self) -> str:
        return self.value[0]

    def get_speed_ratio(self) -> float:
        return self.value[1]

    def get_behavior(self) -> bhvr.GhostBehavior | None:
        return self.value[2]

# General Ghost class
class Ghost(Token):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    state: GhostState | None = None
    target_coord: tuple[float, float] = 0.0, 0.0
    scatter_coord: tuple[float, float] = 0.0, 0.0
    current_bhvr: bhvr.GhostBehavior | None = None


# Red ghost
class Blinky(Ghost):
    ghost_specific_bhvr: bhvr.BlinkyBehavior = bhvr.BlinkyBehavior()
    pass


# Pink ghost
class Pinky(Ghost):
    ghost_specific_bhvr: bhvr.PinkyBehavior = bhvr.PinkyBehavior()
    pass


# Cyan ghost
class Inky(Ghost):
    ghost_specific_bhvr: bhvr.InkyBehavior = bhvr.InkyBehavior()
    pass


# Orange ghost
class Clyde(Ghost):
    ghost_specific_bhvr: bhvr.ClydeBehavior = bhvr.ClydeBehavior()
    pass
