# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

import os
import sys


def get_resource_path(relative_path: str) -> str:
    """
    Returns absolute path to resource, working both in development
    and inside the PyInstaller executable temporary directory.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)