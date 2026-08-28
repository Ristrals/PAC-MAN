# PACMAN - 42Luxembourg 2026 - kmalfois

from src.entity.token import Token


class Pacman(Token):
    is_powered_up: bool = False
    is_invincible: bool = False
