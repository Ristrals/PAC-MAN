# PACMAN - 42Luxembourg 2026 - kmalfois

import json
from pathlib import Path

class ScoreLoader:
    def __init__(self):
        score_board: dict = {}

    # Loads score's JSON file into the game
    def score_load(self):
        score_path: Path = Path(__file__).parent / "data" / "highscore.json"
        
        with open(score_path, "r") as scores:

