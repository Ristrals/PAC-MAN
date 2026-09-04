# PACMAN - 42Luxembourg 2026 - kmalfois
import src.entity as ent


# Pink ghost
class Pinky(ent.Ghost):
    def _chase_behavior(self) -> None:
        self.target_coord = self.pacman.coordinates