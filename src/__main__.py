"""Entry point of the Pac-Man game.

Usage:
    python3 pac-man.py <config.json>

When run as a frozen executable (PyInstaller), the configuration
defaults to ``data/configuration.json``.
"""

import sys
import warnings
import arcade
from arcade.exceptions import PerformanceWarning
from src.config import load_config
from src.main_menu import MainMenuView


def main() -> None:
    """Load the configuration and launch the game window.

    The configuration path is read from the first command-line
    argument. Without it, the program falls back to
    ``data/configuration.json`` when frozen, or prints the usage and
    exits otherwise.

    The window takes 85% of the screen size and opens on the main
    menu.

    Raises:
        SystemExit: If no configuration path is given (outside a
            frozen executable), or if the configuration fails to load.
    """
    warnings.filterwarnings("ignore", category=PerformanceWarning)
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    elif getattr(sys, "frozen", False):
        config_path = "data/configuration.json"
    else:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)
    try:
        config = load_config(config_path)
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
    try:
        arcade.run()
    except KeyboardInterrupt:
        print("Game stopped.")


if __name__ == "__main__":
    main()
