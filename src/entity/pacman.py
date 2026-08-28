# PACMAN - 42Luxembourg 2026 - kmalfois

from math import isclose
from src.entity.token import Token
from src.data_lib import Movements as Mvt
from src.grid.cell import StateType as St
from src.entity.ghost import Ghost, GhostState as Gs


class Pacman(Token):
    is_powered_up: bool = False
    is_invincible: bool = False




