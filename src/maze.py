from src.grid.cell import Cell, StateType


class Maze:
    def __init__(self, width: int, height: int, grid: list[list[Cell]]):
        self.width = width
        self.height = height
        self.grid = grid

    def get_cell(self, x, y) -> Cell:
        return self.grid[y][x]

    def place_items(self) -> None:
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1)
        ]
        for x, y in corners:
            self.get_cell(x, y).state_type = StateType.SUPER_PACGUM