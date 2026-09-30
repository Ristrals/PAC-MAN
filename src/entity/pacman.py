# PACMAN - 42Luxembourg 2026 - kmalfois

from src.data_lib import TextColors as Tc
from src.entity.token import Token
from src.grid.grid_loader import Grid


class Pacman(Token):
    """Represent the player-controlled Pac-Man entity.

    Attributes:
        is_powered_up: Whether Pac-Man can defeat ghosts.
        is_invincible: Whether Pac-Man is temporarily protected from damage.
    """

    is_powered_up: bool = False
    is_invincible: bool = False

    def __str__(self) -> str:
        """Return a formatted description of Pac-Man's current state.

        Returns:
            A string containing Pac-Man's position, directions, and cell.
        """
        name = f"{Tc.ylw}Pacman{Tc.clr}"
        y, x = self.coordinates
        to_print = (
            f"{name} | "
            f"{Tc.ylw}self{Tc.clr}:({y:.3f},{x:.3f}),{Tc.ylw}init{Tc.clr}:{self.init_coord} | "
            f"{Tc.ylw}dir{Tc.clr}:{self.direction.value if self.direction else None},"
            f"{Tc.ylw}buff_dir{Tc.clr}:{self.buffered_direction.value if self.buffered_direction else None} | "
            f"{Tc.ylw}current_cell{Tc.clr}:{self.current_cell.coordinates}"
        )

        return to_print

    def move(self, delta_time: float, grid: Grid) -> None:
        """Move Pac-Man through the grid for one update.

        Args:
            delta_time: Time elapsed since the previous update.
            grid: Grid used to update Pac-Man's current cell.
        """
        if not self.active:
            return

        cy, cx = self.current_cell.coordinates
        center_y, center_x = cy + 0.5, cx + 0.5

        if self.buffered_direction and self.direction:
            if self.buffered_direction == self.direction.opposite:
                if self.can_move(self.buffered_direction):
                    self.direction = self.buffered_direction
                    self.buffered_direction = None

        if self.direction is None:
            if self.buffered_direction and self.can_move(self.buffered_direction):
                self.direction = self.buffered_direction
                self.buffered_direction = None
            else:
                return

        distance_remaining = self.speed * delta_time

        while distance_remaining > 0 and self.direction:
            dir_y, dir_x = self.direction.cell_offset

            # Calculate distance to center along active axis
            if dir_x != 0:
                dist_to_center = (center_x - self.x) if dir_x > 0 else (self.x - center_x)
            else:
                dist_to_center = (center_y - self.y) if dir_y > 0 else (self.y - center_y)

            # If we are heading toward center and this frame's step reaches or overshoots it
            if dist_to_center > 0 and distance_remaining >= dist_to_center:
                # Snap directly to exact cell center
                self.y, self.x = center_y, center_x
                distance_remaining -= dist_to_center

                # Evaluate intersection turns or stops exactly at center
                if self.buffered_direction and self.can_move(self.buffered_direction):
                    self.direction = self.buffered_direction
                    self.buffered_direction = None
                elif not self.can_move(self.direction):
                    self.direction = None
                    break
            else:
                # Normal displacement step
                self.y += dir_y * distance_remaining
                self.x += dir_x * distance_remaining
                distance_remaining = 0.0

            # Update current cell reference when integer coordinates change
        new_cy, new_cx = int(self.y), int(self.x)
        if (new_cy, new_cx) != (cy, cx):
            self.current_cell = grid.get_cell(new_cy, new_cx)
