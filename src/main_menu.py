import arcade
from src.score import ScoreManager


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.options = ["Start", "Exit"]
        self.selected = 0
        try:
            self.score_manager = ScoreManager()
        except Exception:
            self.score_manager = None

    def on_draw(self):
        self.clear()
        screen_width, screen_height = arcade.get_display_size()
        arcade.draw_text(
            "PAC-MAN",
            self.window.width / 2,
            self.window.height * 0.85,
            arcade.color.YELLOW,
            60,
            anchor_x="center",
            bold=True
        )
        arcade.draw_text(
            "Highscores",
            self.window.width / 2,
            self.window.height * 0.85 - 100,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            bold=True
        )
        for i in range(5):
            if self.score_manager and i < len(self.score_manager.score_board):
                entry = self.score_manager.score_board[i]
                text = f"{i + 1}.{entry['name']} - {entry['score']} pts"
            else:
                text = f"{i + 1}. --- - --- pts"
            arcade.draw_text(
                text,
                self.window.width / 8,
                self.window.height * 0.65 - i * 60,
                arcade.color.WHITE,
                15
            )
        for i in range(5):
            idx = i + 5
            if self.score_manager and idx < len(self.score_manager.score_board):
                entry = self.score_manager.score_board[idx]
                text = f"{idx + 1}.{entry['name']} - {entry['score']} pts"
            else:
                text = f"{idx + 1}. --- - --- pts"
            arcade.draw_text(
                text,
                self.window.width / 8 * 5,
                self.window.height * 0.65 - i * 60,
                arcade.color.WHITE,
                15
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
                self.window.width * 0.25 if i == 0 else self.window.width * 0.75,
                120,
                color,
                30,
                anchor_x="center",
                bold=True
            )
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
        if key == arcade.key.LEFT:
            self.selected = 0
        elif key == arcade.key.RIGHT:
            self.selected = 1
        elif key == arcade.key.ENTER:
            if self.selected == 0:
                # start game
                pass
            elif self.selected == 1:
                arcade.close_window()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


if __name__ == "__main__":
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN")
    menu = MainMenuView()
    window.show_view(menu)
    arcade.run()
