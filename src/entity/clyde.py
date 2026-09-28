# PACMAN - 42Luxembourg 2026 - kmalfois

import src.entity as ent


# Orange ghost
class Clyde(ent.Ghost):
    def _chase_behavior(self) -> None:
        if self._get_relative_distance(self.pacman.coordinates) >= 8.0:
            self.target_coord = self.pacman.coordinates
        elif self._get_relative_distance(self.pacman.coordinates) < 8.0:
            self.target_coord = self.scatter_coord
