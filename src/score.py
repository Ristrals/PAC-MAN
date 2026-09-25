# PACMAN - 42Luxembourg 2026 - kmalfois

import json
import re
import os
from typing import Annotated, Any
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError, TypeAdapter
from src.error import ScoreError as ScErr
from src.error import ScoreErrorType as ScErrType


# Score BaseModel
class Score(BaseModel):
    name: Annotated[str, Field(max_length=10, pattern=r"^[a-zA-Z0-9 ]+$", alias="name")]
    score: Annotated[int, Field(ge=0, le=99999, alias="score")]

    @classmethod
    def validation_mitigation(cls, entry_index: int | None = None, **data) -> 'Score':
        try:
            return cls(**data)
        except ValidationError as ve:
            for err in ve.errors():
                val_error_type = err['type']
                val_error_loc = err['loc']
                if val_error_type == "json_invalid":
                    raise ScErr(ScErrType.JSON_CORRUPT, ve, entry_index=entry_index)
                if val_error_type == "missing":
                    raise ScErr(ScErrType.JSON_BADKEY, ve, entry_index=entry_index)
                print(ScErr(ScErrType.SCHEMA_INVALID, ve, entry_index=entry_index))
                if isinstance(val_error_loc, tuple):
                    if "name" in val_error_loc:
                        if val_error_type == "string_too_long":
                            data['name'] = data['name'][:10]
                        elif val_error_type == "string_pattern_mismatch":
                            data['name'] = re.sub(r"[^a-zA-Z0-9\s]", " ", data['name'])[:10]
                        else:
                            data['name'] = "Player"
                    if "score" in val_error_loc:
                        if val_error_type == "less_than_equal":
                            data['score'] = 99999
                        elif val_error_type == "greater_than_equal":
                            data['score'] = 0
                        else:
                            data['score'] = 0
        return cls(**data)


# Score Board BaseModel
class ScoreBoard(BaseModel):
    score_board: list[Score] = Field(default_factory=list)

    @classmethod
    def validation_mitigation(cls, data: str) -> 'ScoreBoard':
        score_board_adapter = TypeAdapter(list[dict])
        try:
            score_board_entries = score_board_adapter.validate_json(data)
        except ValidationError as ve:
            raise ScErr(ScErrType.JSON_CORRUPT, ve)

        mitigated_score_board = [
            Score.validation_mitigation(**entry, entry_index=idx)
            for idx, entry in enumerate(score_board_entries)
        ]
        return cls(score_board=mitigated_score_board)

    @property
    def scores(self) -> list[Score]:
        return self.score_board


# Class responsible for managing scores.
class ScoreManager:
    def __init__(self, highscore_filename: str) -> None:
        self._root_path: Path = Path(__file__).parent.parent
        self._score_directory_path: Path = self._root_path / "data"
        self._score_file_path: Path = self._score_directory_path / f"{highscore_filename}"
        self._is_valid_score_board: bool = True
        self.score_board: list[Score] = []
        self.player_score: Score = Score(name="Player", score=0)

        # File path check
        try:
            self.check_file_path()
        except ScErr as se:
            print(se)
            self.reset_score_board()
            self._is_valid_score_board = False

        # Loading score board from file's data
        if self._is_valid_score_board:
            try:
                self.load_scores()
            except ScErr as se:
                # print(f"{se.err_type}")
                if se.err_type in ("json_invalid", "missing"):
                    print(se)
                    self.reset_score_board()
                    self._is_valid_score_board = False
                else:
                    print(se)
                    self.reset_score_board()

    # String function.
    def __str__(self) -> str:
        score_str = "\n--= SCORE BOARD =--\n"
        for index, score in enumerate(self.score_board, start=1):
            score_str += f"{index} | {score.name}: {score.score}\n"
        return score_str

    # Loads score's JSON file into the game.
    def load_scores(self) -> None:
        with open(self._score_file_path, "r", encoding="utf-8") as scores_list:
            scores_string = scores_list.read()
        self.score_board = ScoreBoard.validation_mitigation(scores_string).scores
        self.score_board.sort(key=lambda score: score.score, reverse=True)

    # Export scores into a JSON file, idealy before the game closes.
    def export_scores(self) -> None:
        entries = [score.model_dump() for score in self.score_board]
        entries_json = json.dumps(entries)
        self.score_board = ScoreBoard.validation_mitigation(entries_json).scores
        if not self._is_valid_score_board:
            os.rename("data/highscores.json", "data/highscores-temp.json")
            self._score_file_path = self._score_directory_path / "highscores.json"
        with open(self._score_file_path, "w", encoding="utf-8") as score_file:
            json.dump([scr.model_dump() for scr in self.score_board], score_file, indent=4)

    # Verify then register an individual score into the score board.
    def register_score(self, player_score: dict[str, Any] | Score) -> None:
        if isinstance(player_score, Score):
            self.player_score = Score.validation_mitigation(**player_score.model_dump())
        else:
            self.player_score = Score.validation_mitigation(**player_score)
        for i in reversed(range(len(self.score_board))):
            if self.score_board[i].name == "Player" and self.score_board[i].score == 0:
                self.score_board.pop(i)
                break
        self.score_board.append(self.player_score)
        self.score_board.sort(key=lambda score: score.score, reverse=True)

    # Checks if highscore file and directory exists in project.
    def check_file_path(self) -> None:
        if not self._score_directory_path.is_dir():
            raise ScErr(ScErrType.DIR_NOT_FOUND, None)
        if not self._score_file_path.is_file():
            raise ScErr(ScErrType.FILE_NOT_FOUND, None)

    # Score board reset option
    def reset_score_board(self) -> None:
        self.score_board = [Score(name="Player", score=0) for i in range(10)]

    # [Tool]: Checks if current score must be recorded.
    def compare_player_score(self, player_score: int) -> bool:
        top_10 = self.get_top_10()
        if len(top_10) < 10:
            return True
        return player_score > top_10[-1].score

    # [Tool]: Returns Top10
    def get_top_10(self) -> list[Score]:
        return self.score_board[:10]


if __name__ == "__main__":
    gaspard: dict = {
        "name": "Gaspard",
        "score": 164
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
        "name": "Tristan",
        "score": 356
    }

    gaspar_score = 164
    jun_score = 125
    kevin_score = 213
    tristan_score = 356

    try:
        score_manager = ScoreManager("highscores.json")
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
        print(score_manager.get_top_10())
        # score_manager.reset_score_board()
        score_manager.export_scores()
    except Exception as e:
        print(e)