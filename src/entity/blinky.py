# PACMAN - 42Luxembourg 2026 - kmalfois
import src.entity as ent
from src.data_lib import Movements as Mvt


# Red ghost
class Blinky(ent.Ghost):
    direction: Mvt = Mvt.RIGHT
    def _chase_behavior(self) -> None:
        self.target_coord = self.pacman.coordinates