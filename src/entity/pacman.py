# PACMAN - 42Luxembourg 2026 - kmalfois

from src.data_lib import TextColors as Tc
from src.entity.token import Token
from src.grid.grid_loader import Grid


class Pacman(Token):
    is_powered_up: bool = False
    is_invincible: bool = False

    def __str__(self) -> str:
        name = f"{Tc.ylw}Pacman{Tc.clr}"
        y, x = self.coordinates
        to_print = (
            f"{name} | "
            f"{Tc.ylw}self{Tc.clr}:({y:.3f},{x:.3f}),init:{self.init_coord} | "
            f"{Tc.ylw}dir{Tc.clr}:{self.direction.value if self.direction else None},"
            f"{Tc.ylw}buff_dir{Tc.clr}:{self.buffered_direction.value if self.buffered_direction else None}"
        )

        return to_print

    def move(self, delta_time: float, grid: Grid) -> None:
        if not self.active:
            return

        cy, cx = self.current_cell.coordinates
        at_center = self.is_cell_centered()

        if self.buffered_direction:
            if self.direction is None or self.buffered_direction == self.direction.opposite:
                if self.can_move(self.buffered_direction):
                    self.direction = self.buffered_direction
                    self.buffered_direction = None
            elif at_center and self.can_move(self.buffered_direction):
                self.direction = self.buffered_direction
                self.y, self.x = cy + 0.5, cx + 0.5
                self.buffered_direction = None

        if self.direction is None:
            return

        if not self.can_move(self.direction) and at_center:
            return

        dir_y, dir_x = self.direction.cell_offset
        self.y += dir_y * self.speed * delta_time
        self.x += dir_x * self.speed * delta_time

        new_cy, new_cx = int(self.y), int(self.x)
        if (new_cy, new_cx) != (cy, cx):
            self.current_cell = grid.get_cell(new_cy, new_cx)
