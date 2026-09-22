# PACMAN - 42Luxembourg 2026 - kmalfois
import src.entity as ent
from src.data_lib import Movements as Mvt


# Cyan ghost
class Inky(ent.Ghost):
    blinky: ent.Ghost
    _PIVOT_OFFSET: dict[Mvt, tuple] = {
        Mvt.UP: (-2.0, -2.0),
        Mvt.DOWN: (2.0, 0.0),
        Mvt.LEFT: (0.0, -2.0),
        Mvt.RIGHT: (0.0, 2.0),
    }

    def _chase_behavior(self) -> None:
        if not self.pacman.direction or not self.blinky:
            self.target_coord = self.pacman.coordinates
            return
        oy, ox = self._PIVOT_OFFSET[self.pacman.direction]
        py, px = self.pacman.coordinates
        by, bx = self.blinky.coordinates
        pivot_y, pivot_x = py + oy, px + ox
        target_y = pivot_y * 2 - by
        target_x = pivot_x * 2 - bx
        self.target_coord = (target_y, target_x)
