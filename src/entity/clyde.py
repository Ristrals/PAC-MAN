# PACMAN - 42Luxembourg 2026 - kmalfois
import src.entity as ent
from src.data_lib import Movements as Mvt


# Orange ghost
class Clyde(ent.Ghost):
    def _chase_behavior(self) -> None:
        self.target_coord = self.pacman.coordinates