# PACMAN - 42Luxembourg 2026 - kmalfois

from abc import ABC
from src.entities.entity import EntityModel
from src.data_lib import Movements
from src.grid.grid_loader import Grid

class Token(EntityModel, ABC):

    def _can_move(self, movement: Movements, grid: Grid) -> bool:
        current_cell = grid.get_cell()
