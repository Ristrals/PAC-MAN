import sys
import argparse
from src.config import load_config
from src.main_menu import MainMenuView
import arcade


def parse_config_path() -> str:
    parser = argparse.ArgumentParser(description="PAC-MAN Game")
    # nargs='?' makes the positional argument optional.
    # If no argument is passed (e.g. on double-click), it defaults to "data/configuration.json".
    parser.add_argument(
        "config_path",
        nargs="?",
        default="data/configuration.json",
        help="Path to configuration file (default: data/configuration.json)"
    )
    args = parser.parse_args()
    return args.config_path


if __name__ == '__main__':
    config_file = parse_config_path()

    try:
        config = load_config(config_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(
        int(screen_width * 0.85),
        int(screen_height * 0.85),
        "PAC-MAN"
    )
    menu = MainMenuView(config)
    window.show_view(menu)
    arcade.run()
