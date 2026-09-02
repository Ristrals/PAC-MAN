# PACMAN - 42Luxembourg 2026 - kmalfois

from src.behavior.ghost import GhostBehavior as Gb


# Returns to initial position when eaten
class EatenBehavior(Gb):
    def get_target(self) -> None:
        py, px = self.pacman.coordinates
        self.target = (float(int(py)) + 0.5), (float(int(px)) + 0.5)