# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from src.entity.token import Token
import src.entity as ent
from src.grid.grid_loader import Grid
from src import behavior as bhvr
from pydantic import ConfigDict, model_validator


# Ghost states
class GhostState(Enum):
    CHASE = ("chase", 0.75)
    SCATTER = ("scatter", 0.75)
    FRIGHTENED = ("frightened", 0.5)
    EATEN = ("eaten", 1.80)

    def get_state(self) -> str:
        return self.value[0]

    def get_speed_ratio(self) -> float:
        return self.value[1]

# General Ghost class
class Ghost(Token):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    state: GhostState | None = GhostState.SCATTER
    target_coord: tuple[float, float] = 0.0, 0.0
    scatter_coord: tuple[float, float] = 0.0, 0.0
    pacman: ent.Pacman
    current_bhvr: bhvr.GhostBehavior | None = None
    ghost_specific_bhvr: bhvr.GhostBehavior | None = None
    scatter_bhvr: bhvr.ScatterBehavior | None = None
    frighten_bhvr: bhvr.FrightenBehavior | None = None
    eaten_bhvr: bhvr.EatenBehavior | None = None

    @model_validator(mode="after")
    def init_behaviors(self) -> 'Ghost':
        self.scatter_bhvr: bhvr.ScatterBehavior = bhvr.ScatterBehavior(ghost=self, pacman=self.pacman)
        self.frighten_bhvr: bhvr.FrightenBehavior = bhvr.FrightenBehavior(ghost=self, pacman=self.pacman)
        self.eaten_bhvr: bhvr.EatenBehavior = bhvr.EatenBehavior(ghost=self, pacman=self.pacman)
        return self

    def update_buffered_direction(self, grid: Grid) -> None:
        """Delegates direction evaluation directly to the active state strategy."""
        match self.state:
            case GhostState.CHASE:
                self.current_bhvr = self.ghost_specific_bhvr
            case GhostState.SCATTER:
                self.current_bhvr = self.scatter_bhvr
            case GhostState.FRIGHTENED:
                self.current_bhvr = self.frighten_bhvr
            case GhostState.EATEN:
                self.current_bhvr = self.eaten_bhvr
            case _:
                self.current_bhvr = None
        if self.current_bhvr:
            self.current_bhvr.update_direction(grid)


# Red ghost
class Blinky(Ghost):
    @model_validator(mode="after")
    def init_behaviors(self) -> 'Blinky':
        self.ghost_specific_bhvr: bhvr.BlinkyBehavior = bhvr.BlinkyBehavior(ghost=self, pacman=self.pacman)
        return self


# Pink ghost
class Pinky(Ghost):
    @model_validator(mode="after")
    def init_behaviors(self) -> 'Pinky':
        self.ghost_specific_bhvr: bhvr.PinkyBehavior = bhvr.PinkyBehavior(ghost=self, pacman=self.pacman)
        return self


# Cyan ghost
class Inky(Ghost):
    blinky: Ghost
    @model_validator(mode="after")
    def init_behaviors(self) -> 'Inky':
        self.ghost_specific_bhvr: bhvr.InkyBehavior = bhvr.InkyBehavior(
            ghost=self, pacman=self.pacman, blinky=self.blinky)
        return self


# Orange ghost
class Clyde(Ghost):
    @model_validator(mode="after")
    def init_behaviors(self) -> 'Clyde':
        self.ghost_specific_bhvr: bhvr.ClydeBehavior = bhvr.ClydeBehavior(ghost=self, pacman=self.pacman)
        return self
