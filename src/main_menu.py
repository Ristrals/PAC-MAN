"""Main menu shown when the game starts."""

from src.score import ScoreManager
from src.config import GameConfig
from src.game_view import GameView


import arcade


class MainMenuView(arcade.View):
    """Main menu displaying the highscores and the Start/Exit options.

    Attributes:
        options: Labels of the menu options.
        selected: Index of the selected option in ``options``.
        score_manager: Manager of the highscore file, or ``None`` if
            it could not be created.
        config: Game configuration, passed to the game view.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize the main menu.

        If the score manager cannot be created, the error is printed
        and no highscores are displayed.

        Args:
            config: Game configuration.
        """
        super().__init__()
        self.options = ["Start", "Exit"]
        self.selected = 0
        self.config = config
        try:
            self.score_manager: ScoreManager | None = ScoreManager(config.highscore_filename)
        except Exception as e:
            print(e)
            self.score_manager = None

    def on_draw(self) -> None:
        """Draw the main menu.

        Draws the title, the top 10 highscores in two columns of five
        (empty slots are shown as ``---``), the Start/Exit options with
        the selected one highlighted, and a bottom bar with the
        controls.
        """
        self.clear()
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
        if self.score_manager:
            entries = self.score_manager.get_top_10()
        else:
            entries = []
        for i in range(5):
            if i < len(entries):
                text = f"{i + 1}.{entries[i].name} - {entries[i].score} pts"
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
            if idx < len(entries):
                text = f"{idx + 1}.{entries[idx].name} - {entries[idx].score} pts"
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

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle the menu navigation.

        Left selects Start and Right selects Exit. Enter confirms the
        selected option: Start opens the game view (if creating it
        fails, the error is printed and the menu stays open), Exit
        closes the window. Escape always closes the window.

        Args:
            key: Code of the pressed key.
            modifiers: Bit mask of the active modifier keys (unused).
        """
        if key == arcade.key.LEFT:
            self.selected = 0
        elif key == arcade.key.RIGHT:
            self.selected = 1
        elif key == arcade.key.ENTER:
            if self.selected == 0:
                try:
                    game_view = GameView(self.config)
                    self.window.show_view(game_view)
                except Exception as e:
                    print(e)
            elif self.selected == 1:
                arcade.close_window()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


if __name__ == "__main__":
    from src.config import load_config
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN")
    menu = MainMenuView(config)
    window.show_view(menu)
    arcade.run()
