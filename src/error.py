# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

from src.data_lib import TextColors as tc

"""Custom exceptions raised by the PacMan."""

class ParsingError(Exception):
    """Raised when the input map file has invalid syntax."""

class ScoreError(Exception):
    def __init__(self, type_err: str, error: Exception | None) -> None:
        self._type_err: str = type_err
        self._message: Exception = error
        self._err_message: str = ""

    def __str__(self):
        self._err_message = f"{tc.red}CaughtScoreError{tc.clr}"