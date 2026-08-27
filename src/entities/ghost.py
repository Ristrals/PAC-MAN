# PACMAN - 42Luxembourg 2026 - kmalfois

from enum import Enum
from src.entities.token import Token
from src.ghost_ai.ghost import Blinky_AI, Pinky_AI, Inky_AI, Clyde_AI, GhostAI


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
    scatter_ai: GhostAI = ScatterAI()
    frighten_ai: GhostAI = FrightenAI()


# Red ghost
class Blinky(Ghost):
    ghost_ai: BlinkyAI = BlinkyAI()
    pass


# Pink ghost
class Pinky(Ghost):
    ghost_ai: PinkyAI = PinkyAI()
    pass


# Cyan ghost
class Inky(Ghost):
    ghost_ai: InkyAI = InkyAI()
    pass


# Orange ghost
class Clyde(Ghost):
    ghost_ai: ClydeAI = ClydeAI()
    pass

