import arcade


from src.config import GameConfig


class GameOverView(arcade.View):
    def __init__(self, score: int, config: GameConfig):
        super().__init__()
        self.score = score
        self.config = config

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )



class VictoryView(arcade.View):
    def __init__(self, score: int, config: GameConfig):
        super().__init__()
        self.score = score
        self.config = config

    def on_draw(self):
        self.clear()


if __name__ == "__main__":
    from src.config import load_config
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = GameOverView(score=1000, config)
    window.show_view(view)
    arcade.run()
