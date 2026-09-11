# PACMAN - 42Luxembourg 2026 - kmalfois

import src.entity as ent
from src.grid.grid_loader import Grid
from src.grid.cell import Cell
from src.data_lib import Movements as Mvt


# Pink ghost
class Pinky(ent.Ghost):
    _TRACKING_OFFSET: dict[Mvt, tuple] = {
        Mvt.UP: (-2.0, 0.0),
        Mvt.DOWN: (2.0, 0.0),
        Mvt.LEFT: (0.0, -2.0),
        Mvt.RIGHT: (0.0, 2.0),
    }
    def _chase_behavior(self) -> None:
        target_cell: Cell
        if self._get_relative_distance(self.pacman.coordinates) <= 2.0:
            self.target_coord = self.pacman.coordinates
        else:
            match self.pacman.direction:
                case Mvt.UP:
                    target_cell = self.grid.get_cell()

    def tracking_ahead_cell(self) -> Cell:
        self.
