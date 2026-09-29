"""End screen shown after a victory or a game over."""

import arcade


from src.config import GameConfig
from src.score import ScoreManager


class EndView(arcade.View):
    """End screen displaying the final score and asking for a name.

    The player types a name, which is saved with the score in the
    highscore file when Enter is pressed. The view then returns to the
    main menu.

    Attributes:
        score: Final score of the game.
        config: Game configuration.
        is_victory: Whether the player won the game.
        player_name: Name typed by the player so far.
        max_name_length: Maximum number of characters of the name.
        score_manager: Manager of the highscore file, or ``None`` if
            it could not be created.
    """

    def __init__(self, score: int, config: GameConfig, is_victory: bool) -> None:
        """Initialize the end screen.

        If the score manager cannot be created, the error is printed
        and scores are not saved.

        Args:
            score: Final score of the game.
            config: Game configuration, used for the highscore
                filename and to go back to the main menu.
            is_victory: Whether the player won the game.
        """
        super().__init__()
        self.score = score
        self.config = config
        self.is_victory = is_victory
        self.player_name = ""
        self.max_name_length = 10
        try:
            self.score_manager: ScoreManager | None = ScoreManager(config.highscore_filename)
        except Exception as e:
            print(e)
            self.score_manager = None

    def on_draw(self) -> None:
        """Clear the screen and draw the end screen."""
        self.clear()
        self.draw_info()
        self.draw_input()

    def draw_info(self) -> None:
        """Draw the title, the final score and the name prompt.

        The title and the message depend on ``is_victory``.
        """
        if self.is_victory:
            title = "YOU WIN!!"
            msg = "Congrats! The ghosts filed a complaint. Name please:"
            color = arcade.color.GREEN
        else:
            title = "GAME OVER..."
            msg = "Who should we blame for this score"
            color = arcade.color.ORANGE
        arcade.draw_text(
            title,
            self.window.width / 2,
            self.window.height * 0.58,
            color,
            50,
            anchor_x="center",
            bold=True
        )
        arcade.draw_text(
            f"FINAL SCORE: {self.score}",
            self.window.width / 2,
            self.window.height * 0.50,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            bold=True
        )
        arcade.draw_text(
            msg,
            self.window.width / 2,
            self.window.height * 0.35,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            bold=True
        )

    def draw_input(self) -> None:
        """Draw the name input box with the typed name and a cursor."""
        arcade.draw_lbwh_rectangle_filled(
            (self.window.width - 300) / 2,
            self.window.height * 0.20,
            300,
            50,
            arcade.color.GRAY
        )
        arcade.draw_lbwh_rectangle_outline(
            (self.window.width - 300) / 2,
            self.window.height * 0.20,
            300,
            50,
            arcade.color.WHITE,
            4
        )
        display_text = self.player_name + "|"
        arcade.draw_text(
            display_text,
            self.window.width / 2,
            self.window.height * 0.2 + 15,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle the name input.

        Letters, digits and spaces are added to the name, up to
        ``max_name_length`` characters. Letters are uppercase when
        Shift is held. Backspace removes the last character. Enter
        saves the score and returns to the main menu, but only if the
        name has at least 3 characters.

        Args:
            key: Code of the pressed key.
            modifiers: Bit mask of the active modifier keys.
        """
        char = chr(key) if 32 <= key <= 126 else None
        if char and (char.isalnum() or char == " "):
            if len(self.player_name) < self.max_name_length:
                if modifiers & arcade.key.MOD_SHIFT:
                    self.player_name += char.upper()
                else:
                    self.player_name += char.lower()

        if key == arcade.key.BACKSPACE:
            self.player_name = self.player_name[:-1]
            return
        if key == arcade.key.ENTER:
            if len(self.player_name) >= 3:
                if self.score_manager:
                    self.score_manager.register_score({
                        "name": self.player_name,
                        "score": self.score
                    })
                    self.score_manager.export_scores()
                from src.main_menu import MainMenuView
                main_menu = MainMenuView(self.config)
                self.window.show_view(main_menu)
        return


if __name__ == "__main__":
    from src.config import load_config
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = EndView(1000, config, True)
    window.show_view(view)
    arcade.run()
