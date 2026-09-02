# PACMAN - 42Luxembourg 2026 - kmalfois

from src.behavior.ghost import GhostBehavior as Gb


# Chases Pacman when far away
# Retreats to scatter corner if 8 tiles from the player
class ClydeBehavior(Gb):
    def get_target(self) -> tuple[float, float]:
        py, px = self.pacman.coordinates
        return (float(int(py)) + 0.5), (float(int(px)) + 0.5)