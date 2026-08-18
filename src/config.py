#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   config.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: junruan <junruan@student.42.fr>              +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/08/17 18:26:14 by junruan             #+#    #+#            #
#   Updated: 2026/08/18 14:50:56 by junruan            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from dataclasses import dataclass, field
from src.error import ParsingError
import json


@dataclass
class LevelConfig:
    width: int = 20
    height: int = 20


@dataclass
class GameConfig:
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    highscore_filename: str = "highscores.json"
    levels: list[LevelConfig] = field(default_factory=list)


def load_config(file_path: str) -> GameConfig:
    if not file_path:
        raise ParsingError("file path is empty")
    try:
        with open(file_path) as file:
            lines = []
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                elif clean_line.startswith("#") or clean_line.startswith("//"):
                    continue
                else:
                    lines.append((clean_line))
        txt = "\n".join(lines)
        data = json.loads(txt)

        config = GameConfig(**data)
        print(config)
    except FileNotFoundError:
        raise ParsingError(f"no file {file_path} detected")


if __name__ == "__main__":
    file_path = "data/configuration.json"
    load_config(file_path)

