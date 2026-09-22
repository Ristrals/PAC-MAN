# PACMAN - 42Luxembourg 2026 - kmalfois

import src.entity as ent
from src.data_lib import Movements as Mvt


# Pink ghost
class Pinky(ent.Ghost):
    _TRACKING_OFFSET: dict[Mvt, tuple] = {
        Mvt.UP: (-4.0, -4.0),
        Mvt.DOWN: (4.0, 0.0),
        Mvt.LEFT: (0.0, -4.0),
        Mvt.RIGHT: (0.0, 4.0),
    }

    def _chase_behavior(self) -> None:
        if not self.pacman.direction:
            self.target_coord = self.pacman.coordinates
            return
        oy, ox = self._TRACKING_OFFSET[self.pacman.direction]
        py, px = self.pacman.coordinates
        self.target_coord = py + oy, px + ox
