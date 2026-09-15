import sys
from src.config import load_config
from src.main_menu import MainMenuView


import arcade


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)
    try:
        config = load_config(sys.argv[1])
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
