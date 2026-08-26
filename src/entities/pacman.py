# PACMAN - 42Luxembourg 2026 - kmalfois

from math import isclose
from src.entities.token import Token
from src.data_lib import Movements as Mvt
from src.grid.cell import StateType as St
from src.entities.ghost import Ghost, GhostState as Gs


class Pacman(Token):
    lives: int = 3
    score: int = 0
    is_powered_up: bool = False
    is_invincible: bool = False

    def select_direction(self, movement: Mvt) -> None:
        self.buffered_direction = movement

    def is_in_collision(self, ghost: Ghost) -> bool:
        if self.is_invincible:
            return False
        if isclose(self.y, ghost.y, abs_tol=0.4) and isclose(self.x, ghost.x, abs_tol=0.4):
            if self.is_powered_up:
                self.score += 200  # TO BE MODIFIED WITH CONFIG DATA
                ghost.state = Gs.EATEN
            else:
                self.lives -= 1
            return True
        return False

    def eat_pacgum(self) -> None:
        if self._is_cell_centered():
            match self.current_cell:
                case St.PACGUM:
                    self.current_cell.state_type = St.EMPTY
                    self.score += 10 # TO BE MODIFIED WITH CONFIG DATA
                case St.SUPER_PACGUM:
                    self.current_cell.state_type = St.EMPTY
                    self.score += 50 # TO BE MODIFIED WITH CONFIG DATA
                    self.is_powered_up = True


