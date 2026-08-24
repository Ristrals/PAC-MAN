# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

from src.config import GameConfig, load_config
from src.score import ScoreManager as Sm
import sys


class Game:
    def __init__(self):
        self.config = load_config(sys.argv[1])
        self.score_board = Sm(self.config.highscore_filename)