# PACMAN - 42Luxembourg 2026 - kmalfois

from src.behavior.ghost import GhostBehavior as Gb


# Cycling around designated corner when not chasing Pacman
class ScatterBehavior(Gb):
    def get_target(self) -> tuple[float, float]:
        py, px = self.pacman.coordinates
        return (float(int(py)) + 0.5), (float(int(px)) + 0.5)