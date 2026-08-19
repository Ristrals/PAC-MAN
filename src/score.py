# PACMAN - 42Luxembourg 2026 - kmalfois

import json
from pydantic import BaseModel, Field, ValidationError, TypeAdapter, field_validator
from typing import Annotated
from pathlib import Path
from src.error import ScoreError as ScErr

# Schema for a score
class Score(BaseModel):
    name: Annotated[str, Field(max_length=10, min_length=3, pattern=r"^[a-zA-Z0-9 ]+$", alias="name")]
    score: Annotated[int, Field(ge=0, alias="score")]

    @field_validator("score", mode="before")
    @classmethod
    def handle_score_threshold(cls, value: object) -> object:
        if isinstance(value, int):
            if value > 99999:
                return 99999
        return value


# Class responsible for managing scores.
class ScoreManager:
    def __init__(self) -> None:
        self._root_path: Path = Path(__file__).parent.parent
        self._score_directory_path: Path = self._root_path / "data"
        self._score_file_path: Path = self._score_directory_path / "highscores.json"
        self.check_file_path()
        self._score_board_valided: bool = True
        self.score_board: list[dict[str, int | str]] = []
        self.load_scores()
        self.player_score: dict[str, int | str] = {}

    # String function.
    def __str__(self) -> str:
        score_str = "\n--= SCORE BOARD =--\n"
        for index, score in enumerate(self.score_board, start=1):
            score_str += f"{index} | {score['name']}: {score['score']}\n"

        return score_str

    # Loads score's JSON file into the game.
    def load_scores(self) -> None:
        with open(self._score_file_path, "r", encoding="utf-8") as scores_list:
            scores_string = scores_list.read()
        self.score_board_validator(scores_string)

    # Export scores into a JSON file, idealy before the game closes.
    def export_scores(self) -> None:
        self.score_board_validator(json.dumps(self.score_board))
        with open(self._score_file_path, "w", encoding="utf-8") as score_file:
            json.dump(self.score_board, score_file, indent=4)

    # Verify then register an individual score into the score board.
    def register_score(self, player_score: dict[str, int | str]) -> None:
        self.score_validator(player_score)
        self.score_board.pop(9)
        self.score_board.append(self.player_score)
        self.score_board.sort(key=lambda score: score['score'], reverse=True)

    # Checks if highscore file and directory exists in project.
    def check_file_path(self) -> None:
        if not self._score_directory_path.is_dir():
            raise ScErr("dir_not_found", None)
        if not self._score_file_path.is_file():
            raise ScErr("file_not_found", None)

    # Score board reset option
    def reset_score_board(self):
        for index, score in enumerate(self.score_board, start=1):
            score['name'] = f"Player{index}"
            score['score'] = 0

    # [Tool]: Checks if current score must be recorded.
    def compare_player_score(self, player_score: int) -> bool:
        if isinstance(self.score_board[9]['score'], int):
            if player_score > self.score_board[9]['score']:
                return True
        return False

    # Validates the entire score board.
    def score_board_validator(self, scores_string: str) -> None:
        _score_adapter = TypeAdapter(list[Score])
        try:
            scores = _score_adapter.validate_json(scores_string)
        except ValidationError as ve:
            if any(error['type'] == "json_invalid"for error in ve.errors()):
                raise ScErr("json_invalid", ve)
            else:
                raise ScErr("schema_invalid", ve)
        if len(scores) != 10:
            raise ScErr("score_count", None)

        self.score_board = [score.model_dump() for score in scores]

    # Will Validate an individual score.
    def score_validator(self, player_score: dict[str, int | str]) -> None:
        _score_adapter = TypeAdapter(Score)
        try:
            _score_adapter.validate_json(json.dumps(player_score))
        except ValidationError as ve:
            if any(error["type"] == "json_invalid"for error in ve.errors()):
                raise ScErr("json_invalid", ve)
            else:
                raise ScErr("schema_invalid", ve)

        self.player_score = player_score

if __name__ == "__main__":
    gaspard: dict = {
        "name" : "Gaspard",
        "score" : 164
    }
    jun: dict = {
        "name": "Jun",
        "score": 125
    }
    kevin: dict = {
        "name": "Kevin",
        "score": 213
    }
    tristan: dict = {
        "name": "Tris tan",
        "score": 356
    }

    gaspar_score = 164
    jun_score = 125
    kevin_score = 213
    tristan_score = 356

    try:
        score_manager = ScoreManager()
        print(score_manager)
        print(
            score_manager.compare_player_score(gaspar_score),
            score_manager.compare_player_score(jun_score),
            score_manager.compare_player_score(kevin_score),
            score_manager.compare_player_score(tristan_score)
        )
        score_manager.register_score(gaspard)
        score_manager.register_score(jun)
        score_manager.register_score(kevin)
        score_manager.register_score(tristan)
        print(score_manager)
        score_manager.export_scores()
    except Exception as e:
        print(e)