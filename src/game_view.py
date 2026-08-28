from src.config import GameConfig, load_config
from src.grid.grid_loader import Grid
from src.grid.cell import StateType
from src.end_view import EndView


import arcade


class GameView(arcade.View):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.grid = Grid(
            config.levels[0].width,
            config.levels[0].height,
            config.seed
        )
        self.config = config
        self.grid.place_items(config.pacgum)
        cell_size_w = (self.window.width * 0.6) / self.grid.width
        cell_size_h = (self.window.height * 0.6) / self.grid.height
        self.cell_size = min(cell_size_w, cell_size_h)
        self.offset_x = (self.window.width - self.grid.width * self.cell_size) / 2
        self.offset_y = (self.window.height - self.grid.height * self.cell_size) / 2
        self.pause = False
        self.options = ["RESUME", "MAIN MENU"]
        self.selected = 0
        self.current_level = 1
        self.time_left = config.level_max_time
        self.score = 0

    def on_draw(self):
        self.clear()
        self.draw_maze()
        self.draw_items()
        self.draw_hud()
        self.draw_page()
        if self.pause:
            self.draw_pause_menu()

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
                        6
                    )
                if not cell.east:
                    arcade.draw_line(
                        px + self.cell_size,
                        py + self.cell_size,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        6
                    )
                if not cell.south:
                    arcade.draw_line(
                        px,
                        py,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        6
                    )
                if not cell.west:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px,
                        py,
                        arcade.color.WHITE,
                        6
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
                        arcade.color.BLUE
                    )
                elif cell.state_type == StateType.PACGUM:
                    arcade.draw_circle_filled(
                        center_x,
                        center_y,
                        self.cell_size * 0.15,
                        arcade.color.BLUE
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
            "❤️" * self.config.lives,
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

    def on_update(self, delta_time):
        if not self.pause:
            self.time_left -= delta_time
            if self.time_left <= 0 or self.lives <= 0:
                self.window.show_view(EndView(self.score, self.config, False))
            if self.current_level > len(self.config.levels):
                self.window.show_view(EndView(self.score, self.config, True))


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = GameView(config)
    window.show_view(view)
    arcade.run()
