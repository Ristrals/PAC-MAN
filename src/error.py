# PACMAN - 42Luxembourg 2026 - juruan, kmalfois

from src.data_lib import TextColors as Tc
from pydantic import ValidationError
from enum import Enum

"""Custom exceptions raised by the PacMan."""

class ParsingError(Exception):
    """Raised when the input map file has invalid syntax."""

# ScoreManager Error types
class ScoreErrorType(Enum):
    # (err_type, is_critical)
    FILE_NOT_FOUND = ("file_not_found", False)
    DIR_NOT_FOUND = ("dir_not_found", False)
    SCHEMA_INVALID = ("schema_invalid", False)
    JSON_CORRUPT = ("json_invalid", False)

    def __init__(self, err_type: str, is_critical: bool) -> None:
        self._err_type: str = err_type
        self._is_critical: bool = is_critical

    @property
    def err_type(self) -> str:
        return self._err_type

    @property
    def is_critical(self) -> bool:
        return self._is_critical

class ScoreError(Exception):

    def __init__(self, err_type: ScoreErrorType, score_error: Exception | None) -> None:
        self._err_type: str = err_type.err_type
        self._is_critical: bool = err_type.is_critical
        self._score_error: Exception | None = score_error
        self._err_message: str = ""

    def __str__(self) -> str:
        _input: str = ""
        _location: str = ""
        _msg: str = ""

        if self._err_type == "file_not_found":
            self._err_message += (f"{Tc.ylw}File 'highscores.json' could not be found{Tc.clr}\n"
                                  f"{Tc.red}[!]No scores will be recorded{Tc.clr}\n")

        if self._err_type == "dir_not_found":
            self._err_message += (f"{Tc.ylw}Directory 'data' could not be found{Tc.clr}\n"
                                  f"{Tc.red}[!]No scores will be recorded{Tc.clr}\n")

        self._err_message = f"{Tc.red}[!]CaughtScoreError{Tc.clr}:\n"
        if self._err_type == "schema_invalid":
            assert isinstance(self._score_error, ValidationError)
            if len(self._score_error.errors()) > 0:
                _input = str(self._score_error.errors()[0]['input'])
                _location = (f"line {self._score_error.errors()[0]['loc'][0]} at "
                                  f"key '{self._score_error.errors()[0]['loc'][1]}'")
                _msg = f"line {self._score_error.errors()[0]['msg']}"
                self._err_message += (
                    f"{Tc.ylw}Input '{_input}' ({_location}) is incorrect.\n"
                    f"{_msg}.{Tc.clr}\n"
                    f"{Tc.red}[!]No scores will be recorded{Tc.clr}\n"
                )
            else:
                self._err_message += (f"{Tc.ylw}Invalid JSON schema.{Tc.clr}\n"
                                      f"{Tc.red}[!]No scores will be recorded{Tc.clr}\n")

        if self._err_type == "json_invalid":
            assert isinstance(self._score_error, ValidationError)
            if len(self._score_error.errors()) > 0:
                _msg = f"{self._score_error.errors()[0]['msg']}"
                self._err_message += f"{Tc.ylw}{_msg}.{Tc.clr}\n"
            else:
                self._err_message += (f"{Tc.ylw}JSON data corrupted.{Tc.clr}\n"
                                      f"{Tc.red}[!]No scores will be recorded{Tc.clr}\n")

        return self._err_message
