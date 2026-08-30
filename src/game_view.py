from src.config import GameConfig, load_config
from src.grid.grid_loader import Grid
from src.grid.cell import StateType
from src.end_view import EndView
from src.data_lib import Movements

import arcade


class GameView(arcade.View):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.config = config
        self.current_level = 1
        self.load_level()
        self.pause = False
        self.cheat_mode = False
        self.invincible = False
        self.ghost_freeze = False
        self.lives = config.lives
        self.options = ["RESUME", "MAIN MENU"]
        self.selected = 0
        self.score = 0

    def calculate_render_params(self):
        cell_size_w = (self.window.width * 0.6) / self.grid.width
        cell_size_h = (self.window.height * 0.6) / self.grid.height
        self.cell_size = min(cell_size_w, cell_size_h)
        self.offset_x = (self.window.width - self.grid.width * self.cell_size) / 2
        self.offset_y = (self.window.height - self.grid.height * self.cell_size) / 2

    def load_level(self):
        level_config = self.config.levels[self.current_level - 1]
        seed = self.config.seed if self.current_level == 1 else None
        self.grid = Grid(
            level_config.width,
            level_config.height,
            seed
        )
        self.grid.place_items(self.config.pacgum)
        from src.entity.pacman import Pacman
        center_cell = self.grid.get_cell(self.grid.width // 2, self.grid.height // 2)
        self.pacman = Pacman(
            y=center_cell.y + 0.5,
            x=center_cell.x + 0.5,
            current_cell=center_cell,
            speed=4.0,
            active=True
        )
        self.time_left = self.config.level_max_time
        self.calculate_render_params()

    def next_level(self):
        self.current_level += 1
        if self.current_level > len(self.config.levels):
            self.window.show_view(EndView(self.score, self.config, True))
            return
        self.load_level()

    def on_draw(self):
        self.clear()
        self.draw_maze()
        self.draw_items()
        self.draw_pacman()
        self.draw_hud()
        self.draw_page()
        if self.pause:
            self.draw_pause_menu()
        if self.cheat_mode:
            self.draw_cheat_panel()

    def draw_maze(self):
        for row in self.grid.grid:
            for cell in row:
                px = self.offset_x + cell.x * self.cell_size
                py = self.offset_y + (self.grid.height - 1 - cell.y) * self.cell_size
                if not any([cell.north, cell.east, cell.south, cell.west]):
                    arcade.draw_lbwh_rectangle_filled(
                        px,
                        py,
                        self.cell_size,
                        self.cell_size,
                        arcade.color.BLUE
                    )
                if not cell.north:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px + self.cell_size,
                        py + self.cell_size,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.east:
                    arcade.draw_line(
                        px + self.cell_size,
                        py + self.cell_size,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.south:
                    arcade.draw_line(
                        px,
                        py,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.west:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px,
                        py,
                        arcade.color.WHITE,
                        1
                    )

    def draw_items(self):
        for row in self.grid.grid:
            for cell in row:
                px = self.offset_x + cell.x * self.cell_size
                py = self.offset_y + (self.grid.height - 1 - cell.y) * self.cell_size
                center_x = px + self.cell_size / 2
                center_y = py + self.cell_size / 2
                if cell.state_type == StateType.SUPER_PACGUM:
                    arcade.draw_circle_filled(
                        center_x,
                        center_y,
                        self.cell_size * 0.25,
                        arcade.color.PINK
                    )
                elif cell.state_type == StateType.PACGUM:
                    arcade.draw_circle_filled(
                        center_x,
                        center_y,
                        self.cell_size * 0.15,
                        arcade.color.YELLOW
                    )

    def draw_pacman(self):
        px = self.offset_x + self.pacman.x * self.cell_size
        py = self.offset_y + (self.grid.height - 1 - self.pacman.y) * self.cell_size
        arcade.draw_circle_filled(
            px,
            py,
            self.cell_size * 0.4,
            arcade.color.YELLOW
        )

    def draw_cheat_panel(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )
        cheat = [
            f"[I] Invincible: {'ON' if self.invincible else 'OFF'}",
            "[N] Skip Level",
            f"[F] Freeze Ghosts: {'ON' if self.ghost_freeze else 'OFF'}",
            f"[L] Add Life ({self.lives})"
        ]
        for i, text in enumerate(cheat):
            arcade.draw_text(
                text,
                self.window.width / 2,
                self.window.height / 2 + 50 - i * 80,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                bold=True
            )

    def draw_hud(self):
        '''
        arcade.draw_lbwh_rectangle_filled(
            0,
            self.window.height - 40,
            self.window.width,
            self.window.height,
            arcade.color.ORANGE
        )
        '''
        arcade.draw_text(
            "❤️" * self.lives,
            self.window.width / 10,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"LEVEL: {self.current_level}",
            self.window.width / 10 * 3,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"SCORE: {self.score}",
            self.window.width / 10 * 6,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"TIMER: {int(self.time_left)}",
            self.window.width / 10 * 9,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def draw_pause_menu(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = arcade.color.BLUE
                prefix = ">"
            else:
                color = arcade.color.WHITE
                prefix = " "
            arcade.draw_text(
                prefix + option,
                self.window.width / 2,
                self.window.height * 0.85 - 200 if i == 0 else self.window.height * 0.85 - 400,
                color,
                24,
                anchor_x="center",
                bold=True
            )

    def draw_page(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            60,
            arcade.color.ORANGE
        )
        arcade.draw_text(
            "DIRECTIONS: ↑ ↓ ← →",
            self.window.width / 4,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )
        arcade.draw_text(
            "PAUSE: P",
            self.window.width / 4 * 2,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )
        arcade.draw_text(
            "CHEAT MODE: C",
            self.window.width / 4 * 3,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        # pause menu
        if key == arcade.key.P:
            self.pause = not self.pause
            return

        if self.pause:
            if key == arcade.key.UP:
                self.selected = 0
            elif key == arcade.key.DOWN:
                self.selected = 1
            elif key == arcade.key.ENTER:
                if self.selected == 0:
                    self.pause = not self.pause
                elif self.selected == 1:
                    from src.main_menu import MainMenuView
                    menu = MainMenuView(load_config("data/configuration.json"))
                    self.window.show_view(menu)
            return

        # cheat mode
        if key == arcade.key.C:
            self.cheat_mode = not self.cheat_mode
            return

        if self.cheat_mode:
            if key == arcade.key.I:
                self.invincible = not self.invincible
            elif key == arcade.key.N:
                if self.current_level < len(self.config.levels):
                    self.next_level()
            elif key == arcade.key.F:
                self.ghost_freeze = not self.ghost_freeze
            elif key == arcade.key.L:
                self.lives += 1
            return

        # pacman move
        if key == arcade.key.UP:
            self.pacman.buffered_direction = Movements.UP
        elif key == arcade.key.DOWN:
            self.pacman.buffered_direction = Movements.DOWN
        elif key == arcade.key.LEFT:
            self.pacman.buffered_direction = Movements.LEFT
        elif key == arcade.key.RIGHT:
            self.pacman.buffered_direction = Movements.RIGHT

    def on_update(self, delta_time):
        if not self.pause:
            self.time_left -= delta_time
            if self.time_left <= 0 or self.lives <= 0:
                self.window.show_view(EndView(self.score, self.config, False))
            if self.current_level > len(self.config.levels):
                self.window.show_view(EndView(self.score, self.config, True))

        self.pacman.move(delta_time, self.grid)
        if self.pacman.is_cell_centered():
            if self.pacman.current_cell.state_type == StateType.PACGUM:
                self.pacman.current_cell.state_type = StateType.EMPTY
                self.score += self.config.points_per_pacgum


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = GameView(config)
    window.show_view(view)
    arcade.run()
