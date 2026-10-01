#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   config.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/17 18:26:14 by junruan             #+#    #+#            #
#   Updated: 2026/10/01 16:21:47 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Game configuration models and loader."""

from pydantic import BaseModel, Field, ValidationError
from pydantic import ValidationInfo, field_validator
from src.error import ParsingError
import json
from pathlib import Path


class LevelConfig(BaseModel):
    """Size of the maze for one level.

    Attributes:
        width: Number of columns of the maze, between 5 and 25.
            Defaults to 15.
        height: Number of rows of the maze, between 5 and 25.
            Defaults to 15.
    """

    width: int = Field(default=15, ge=5)
    height: int = Field(default=15, ge=5)

    @field_validator("width", "height", mode="before")
    @classmethod
    def clamp_positive_int(cls, v: object, info: ValidationInfo) -> int:
        """Replace an invalid width or height with its default value.

        Args:
            v: Raw value read from the configuration.
            info: Validation context, used to get the field name.

        Returns:
            ``v`` if it is an integer between 5 and 25, otherwise the
            field's default value (a warning is printed).
        """
        field_name = info.field_name
        if field_name is None:
            return v if isinstance(v, int) else 15
        default = int(cls.model_fields[field_name].default)
        if not isinstance(v, int) or v < 5 or v > 25:
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v


class GameConfig(BaseModel):
    """Global configuration of the game.

    Invalid values are replaced by their default with a warning
    instead of raising an error.

    Attributes:
        lives: Number of lives of the player. Defaults to 3.
        pacgum: Number of pacgums placed in each maze. Defaults to 42.
        points_per_pacgum: Score for eating a pacgum. Defaults to 10.
        points_per_super_pacgum: Score for eating a super pacgum.
            Defaults to 50.
        points_per_ghost: Score for eating a ghost. Defaults to 200.
        seed: Seed used for the maze generation. Defaults to 42.
        level_max_time: Time limit of a level, in seconds.
            Defaults to 90.
        highscore_filename: File where the highscores are saved.
            Defaults to ``"highscores.json"``.
        levels: Size of the maze for each level. Defaults to an
            empty list; ``load_config`` adds a default level when
            it is empty.
    """

    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=1)
    points_per_pacgum: int = Field(default=10, ge=1)
    points_per_super_pacgum: int = Field(default=50, ge=1)
    points_per_ghost: int = Field(default=200, ge=1)
    seed: int = Field(default=42, ge=1)
    level_max_time: int = Field(default=90, ge=1)
    highscore_filename: str = "highscores.json"
    levels: list[LevelConfig] = Field(default_factory=list)

    @field_validator(
        "lives",
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "seed",
        "level_max_time",
        mode="before"
    )
    @classmethod
    def clamp_positive_int(cls, v: object, info: ValidationInfo) -> int:
        """Replace an invalid numeric value with its default value.

        Args:
            v: Raw value read from the configuration.
            info: Validation context, used to get the field name.

        Returns:
            ``v`` if it is an integer greater than or equal to 1,
            otherwise the field's default value (a warning is printed).
        """
        field_name = info.field_name
        assert field_name is not None
        default = int(cls.model_fields[field_name].default)
        if not isinstance(v, int) or v < 1:
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def clamp_filename_value(cls, v: object, info: ValidationInfo) -> str:
        """Replace a non-string highscore filename with its default.

        Args:
            v: Raw value read from the configuration.
            info: Validation context, used to get the field name.

        Returns:
            ``v`` if it is a string, otherwise the field's default
            value (a warning is printed).
        """
        field_name = info.field_name
        assert field_name is not None
        default = str(cls.model_fields[field_name].default)
        if not isinstance(v, str):
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        path = Path(v)
        if path.suffix.lower() != ".json" or not path.stem.strip():
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v


def strip_comments(text: str) -> str:
    """Remove comments from a JSON-like text.

    Supported comments are ``/* ... */`` blocks, and ``#`` or ``//``
    until the end of the line. Comment markers inside strings are
    kept. Newlines inside block comments are kept so that JSON error
    line numbers still match the original file.

    Args:
        text: Raw content of the configuration file.

    Returns:
        The text without comments.

    Raises:
        ParsingError: If a block comment is never closed.
    """
    result: list[str] = []
    in_string = False
    in_block = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_block:
            if c == "*" and nxt == "/":
                in_block = False
                result.append(" ")
                i += 2
                continue
            if c == "\n":
                result.append(c)
            i += 1
        elif in_string:
            result.append(c)
            if c == "\\" and nxt:
                result.append(nxt)
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
        elif c == '"':
            in_string = True
            result.append(c)
            i += 1
        elif c == "/" and nxt == "*":
            in_block = True
            i += 2
        elif c == "#" or (c == "/" and nxt == "/"):
            while i < n and text[i] != "\n":
                i += 1
        else:
            result.append(c)
            i += 1
    if in_block:
        raise ParsingError("unclosed block comment")
    return "".join(result)


def load_config(file_path: str) -> GameConfig:
    """Load the game configuration from a JSON file.

    Comments are removed with ``strip_comments`` before parsing.
    A warning is printed for each missing key, which then takes its
    default value. The configuration falls back to the defaults, with
    a warning, if the JSON root is not an object or if the data does
    not pass validation. If ``levels`` ends up empty, one default
    level is added.

    Args:
        file_path: Path to the configuration file.

    Returns:
        The loaded configuration, with at least one level.

    Raises:
        ParsingError: If the path is empty, the file does not exist,
            a block comment is never closed, or the content is not
            valid JSON.
    """
    if not file_path:
        raise ParsingError("file path is empty")
    try:
        with open(file_path) as file:
            txt = strip_comments(file.read())
        try:
            data = json.loads(txt)
            if not isinstance(data, dict):
                print("Warning: config is not a JSON object, using defaults.")
                return GameConfig(levels=[LevelConfig()])
            expected_keys = [
                "lives",
                "seed",
                "pacgum",
                "points_per_pacgum",
                "points_per_super_pacgum",
                "points_per_ghost",
                "level_max_time",
                "highscore_filename",
                "levels"
            ]
            for key in expected_keys:
                if key not in data:
                    print(f"Warning: {key} missing, using default.")
        except json.JSONDecodeError:
            raise ParsingError("json format error detected")
        try:
            config = GameConfig(**data)
        except ValidationError as e:
            print(f"Warning: {e}")
            config = GameConfig()
        if not config.levels:
            print("Warning: levels is empty, using default.")
            config.levels = [LevelConfig()]
        return config
    except FileNotFoundError:
        raise ParsingError(f"no file {file_path} detected")


if __name__ == "__main__":
    file_path = "data/configuration.json"
    load_config(file_path)
