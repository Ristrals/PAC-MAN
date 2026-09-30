# PACMAN - 42Luxembourg 2026 - kmalfois
import src.entity as ent


# Red ghost
class Blinky(ent.Ghost):
    """Represent Blinky, the red ghost that directly chases Pac-Man."""

    def _chase_behavior(self) -> None:
        """Set Pac-Man's current position as Blinky's target."""
        self.target_coord = self.pacman.coordinates
