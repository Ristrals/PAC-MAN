from src.config import GameConfig
from src.grid.grid_loader import Grid
from src.grid.cell import StateType
import arcade


class GameView(arcade.View):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.grid = Grid(
            config.levels[0].width,
            config.levels[0].height,
            config.seed
        )
        self.grid.place_items(config.pacgum)
        cell_size_w = (self.window.width * 0.6) / self.grid.width
        cell_size_h = (self.window.height * 0.6) / self.grid.height
        self.cell_size = min(cell_size_w, cell_size_h)
        self.offset_x = (self.window.width - self.grid.width * self.cell_size) / 2
        self.offset_y = (self.window.height - self.grid.height * self.cell_size) / 2

    def on_draw(self):
        self.clear()
        self.draw_maze()
        self.draw_items()
        self.draw_page()

    def draw_maze(self):
        for row in self.grid.grid:
            for cell in row:
                px = self.offset_x + cell.x * self.cell_size
                py = self.offset_y + (self.grid.height - 1 - cell.y) * self.cell_size
                if not cell.north:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px + self.cell_size,
                        py + self.cell_size,
                        arcade.color.WHITE,
                        10
                    )
                if not cell.east:
                    arcade.draw_line(
                        px + self.cell_size,
                        py + self.cell_size,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        10
                    )
                if not cell.south:
                    arcade.draw_line(
                        px,
                        py,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        10
                    )
                if not cell.west:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px,
                        py,
                        arcade.color.WHITE,
                        10
                    )
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            60,
            arcade.color.ORANGE
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

    def draw_page(self):
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
        arcade.draw_text(
            "PAC-MAN",
            self.window.width / 2,
            self.window.height * 0.85,
            arcade.color.YELLOW,
            60,
            anchor_x="center",
            bold=True
        )


if __name__ == "__main__":
    from src.config import load_config
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = GameView(config)
    window.show_view(view)
    arcade.run()
