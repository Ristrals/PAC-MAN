# PACMAN - 42Luxembourg 2026 - kmalfois

from math import isclose
from enum import Enum
from src.entities.token import Token
from src.entities.ghost_ai import Blinky_AI, Pinky_AI, Inky_AI, Clyde_AI
from src.data_lib import Movements as Mvt
from src.grid.grid_loader import Grid
from src.grid.cell import Cell, StateType as St


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


# Red ghost
class Blinky(Ghost):
    ghost_ai: GhostAI = BlinkyAI()
    pass


# Pink ghost
class Pinky(Ghost):
    ghost_ai: GhostAI = PinkyAI()
    pass


# Cyan ghost
class Inky(Ghost):
    ghost_ai: GhostAI = InkyAI()
    pass


# Orange ghost
class Clyde(Ghost):
    ghost_ai: GhostAI = ClydeAI()
    pass

