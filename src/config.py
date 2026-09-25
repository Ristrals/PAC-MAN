#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   config.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/17 18:26:14 by junruan             #+#    #+#            #
#   Updated: 2026/09/19 16:44:35 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ValidationError
from pydantic import ValidationInfo, field_validator
from src.error import ParsingError
import json


class LevelConfig(BaseModel):
    width: int = Field(default=15, ge=5)
    height: int = Field(default=15, ge=5)

    @field_validator("width", "height", mode="before")
    @classmethod
    def clamp_positive_int(cls, v: object, info: ValidationInfo) -> int:
        field_name = info.field_name
        if field_name is None:
            return v if isinstance(v, int) else 15
        default = cls.model_fields[field_name].default
        if not isinstance(v, int) or v < 5 or v > 25:
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v


class GameConfig(BaseModel):
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
        field_name = info.field_name
        assert field_name is not None
        default = cls.model_fields[field_name].default
        if not isinstance(v, int) or v < 1:
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def clamp_filename_value(cls, v: object, info: ValidationInfo) -> str:
        field_name = info.field_name
        assert field_name is not None
        default = cls.model_fields[field_name].default
        if not isinstance(v, str):
            print(f"Warning: {field_name} = {v} invalid, using {default}")
            return default
        return v


def load_config(file_path: str) -> GameConfig:
    if not file_path:
        raise ParsingError("file path is empty")
    try:
        with open(file_path) as file:
            lines = []
            comment_block = False
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                if comment_block:
                    if "*/" in clean_line:
                        comment_block = False
                        clean_line = clean_line.split("*/")[1]
                        if not clean_line:
                            continue
                    else:
                        continue
                if "/*" in clean_line:
                    comment_block = True
                    clean_line = clean_line.split("/*")[0]
                    if not clean_line:
                        continue
                elif "#" in clean_line:
                    clean_line = clean_line.split("#")[0]
                    if not clean_line:
                        continue
                elif "//" in clean_line:
                    clean_line = clean_line.split("//")[0]
                    if not clean_line:
                        continue
                lines.append((clean_line))
        txt = "\n".join(lines)
        try:
            data = json.loads(txt)
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
        return config
    except FileNotFoundError:
        raise ParsingError(f"no file {file_path} detected")


if __name__ == "__main__":
    file_path = "data/configuration.json"
    load_config(file_path)
