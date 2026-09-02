# PACMAN - 42Luxembourg 2026 - kmalfois

from src.behavior.ghost import GhostBehavior as Gb


# Spooked when Pacman's powered up
class FrightenBehavior(Gb):
    def get_target(self) -> None:
        py, px = self.pacman.coordinates
        self.target = (float(int(py)) + 0.5), (float(int(px)) + 0.5)