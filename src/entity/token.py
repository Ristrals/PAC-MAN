# PACMAN - 42Luxembourg 2026 - kmalfois

from abc import ABC, abstractmethod
from math import isclose
from pydantic import BaseModel, model_validator
from src.data_lib import Movements as Mvt
from src.grid.grid_loader import Grid
from src.grid.cell import Cell


class Token(BaseModel, ABC):
    """Base model for movable Pac-Man and ghost entities.

    Attributes:
        y: Vertical coordinate of the token.
        x: Horizontal coordinate of the token.
        speed: Movement speed of the token.
        current_cell: Grid cell currently occupied by the token.
        direction: Current movement direction, if one is set.
        buffered_direction: Movement direction waiting to be applied.
        active: Whether the token is currently active.
        init_coord: Initial coordinates used when resetting the token.
        init_cell: Initial cell used when resetting the token.
    """

    y: float = 0.0
    x: float = 0.0
    speed: float = 0.0
    current_cell: Cell
    direction: Mvt | None = None
    buffered_direction: Mvt | None = None
    active: bool = True

    # Initial position in case of reset
    init_coord: tuple[float, float] | None = None
    init_cell: Cell | None = None

    # Sets initial position after item creation
    @model_validator(mode="after")
    def _set_initial_position(self) -> 'Token':
        """Set initial coordinates and cell after the token is created.

        Returns:
            The initialized token.
        """
        if self.init_coord is None:
            self.init_coord = (self.y, self.x)
        if self.init_cell is None:
            self.init_cell = self.current_cell
        return self

    # Reset token to initial position
    def reset_position(self) -> None:
        """Restore the token to its initial coordinates and cell."""
        assert (
            isinstance(self.init_cell, Cell) and
            isinstance(self.init_coord, tuple)
        )
        self.y, self.x = self.init_coord
        self.current_cell = self.init_cell

    # Movement
    @abstractmethod
    def move(self, delta_time: float, grid: Grid) -> None:
        """Move the token according to elapsed time and the current grid.

        Args:
            delta_time: Time elapsed since the previous update.
            grid: Grid used to update the token's current cell.
        """
        pass

    # Check if token is at cell center
    def is_cell_centered(self) -> bool:
        """Return whether the token is close to the center of its cell.

        Returns:
            ``True`` when the token is within the cell-centering tolerance.
        """
        cy, cx = self.current_cell.coordinates
        return (
            isclose(self.y, cy + 0.5, abs_tol=0.08) and
            isclose(self.x, cx + 0.5, abs_tol=0.08)
        )

    # Return if the entity is allowed to move in current direction
    def can_move(self, direction: Mvt | None) -> bool:
        """Check whether the current cell allows movement in a direction.

        Args:
            direction: Direction to check, or ``None``.

        Returns:
            Whether the token can leave its current cell in that direction.
        """
        match direction:
            case Mvt.UP: return self.current_cell.north
            case Mvt.DOWN: return self.current_cell.south
            case Mvt.LEFT: return self.current_cell.west
            case Mvt.RIGHT: return self.current_cell.east
            case _: return False

    # [Properties]
    @property
    def coordinates(self) -> tuple[float, float]:
        """Return the token's coordinates as a ``(y, x)`` tuple."""
        return self.y, self.x

    @coordinates.setter
    def coordinates(self, value: tuple[float, float] | None) -> None:
        """Set the token's coordinates.

        Args:
            value: New coordinates as a ``(y, x)`` tuple.
        """
        assert isinstance(value, tuple)
        self.y, self.x = value

    @property
    def current_direction(self) -> Mvt | None:
        """Return the token's current movement direction."""
        return self.direction

    @property
    def input_direction(self) -> Mvt | None:
        """Return the token's buffered input direction."""
        return self.buffered_direction

    @input_direction.setter
    def input_direction(self, value: Mvt | None) -> None:
        """Set the token's buffered input direction.

        Args:
            value: Direction to buffer, or ``None`` to clear it.
        """
        self.buffered_direction = value
