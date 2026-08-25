from mazegenerator import MazeGenerator
from src.config import load_config
from src.grid.cell import Cell, StateType, create_cell
import random


class Grid:
    def __init__(self, width: int, height: int, seed: int | None) -> None:
        self.width: int = width
        self.height: int = height
        self.seed: int | None = seed
        self.grid: list[list[Cell]] = []
        self.maze_load()

    def maze_load(self) -> None:
        try:
            m = MazeGenerator(size=(self.width, self.height), perfect=False)
            if isinstance(self.seed, int):
                m.generate(seed=self.seed)
        except Exception as e:
            raise Exception(f"Error: maze generation is failed, {e}")
        if not m.maze:
            raise Exception("Error: maze data is empty")
        grid: list[list[Cell]] = []
        for y, row in enumerate(m.maze):
            row_cells: list[Cell] = []
            for x, value in enumerate(row):
                cell = create_cell(x, y, value)
                row_cells.append(cell)
            grid.append(row_cells)
        self.grid = grid

    def get_cell(self, x, y) -> Cell:
        return self.grid[y][x]

    def place_items(self, pacgum_count: int) -> None:
        count = pacgum_count
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1)
        ]
        for x, y in corners:
            self.get_cell(x, y).state_type = StateType.SUPER_PACGUM
        maze_center = self.get_cell(self.width // 2, self.height // 2)
        available = []
        for row in self.grid:
            for cell in row:
                if (cell.state_type == StateType.EMPTY
                        and cell is not maze_center
                        and any([cell.north, cell.east, cell.south, cell.west])):
                    available.append(cell)
        if count > len(available):
            print(
                f"Warning: requested {count} pacgum but only "
                f"{len(available)} cells available, clamping"
            )
            count = len(available)
        selected = random.sample(available, count)
        for cell in selected:
            cell.state_type = StateType.PACGUM


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    # Niveau 1
    grid1 = Grid(
        width=config.levels[0].width,
        height=config.levels[0].height,
        seed=config.seed
    )
    grid1.place_items(config.pacgum)
