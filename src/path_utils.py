# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    path_obj = Path(relative_path)
    if path_obj.is_absolute():
        return path_obj

    if getattr(sys, "frozen", False):
        # 1. Bundled inside PyInstaller's _internal directory (sys._MEIPASS)
        bundle_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent)) / path_obj
        if bundle_path.exists():
            return bundle_path

        # 2. Located right next to the executable (dist/pacman_game/data/...)
        exe_path = Path(sys.executable).parent / path_obj
        if exe_path.exists():
            return exe_path

    # 3. Running in dev environment (current working directory or project root)
    return path_obj.resolve()