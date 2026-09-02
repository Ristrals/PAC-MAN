# PACMAN - 42Luxembourg 2026 - kmalfois

from src.behavior.ghost import GhostBehavior as Gb


# Targets 4 tiles ahead of Pacman's direction
class PinkyBehavior(Gb):
    def get_target(self) -> tuple[float, float]:
        py, px = self.pacman.coordinates
        return (float(int(py)) + 0.5), (float(int(px)) + 0.5)