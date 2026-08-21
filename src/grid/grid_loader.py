from mazegenerator import MazeGenerator
from src.config import load_config
from src.grid.cell import Cell, create_cell

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
            print(f"Error: maze generation is failed, {e}")
        if not m.maze:
            print("Error: maze data is empty")
        grid: list[list[Cell]] = []
        for y, row in enumerate(m.maze):
            row_cells: list[Cell] = []
            for x, value in enumerate(row):
                cell = create_cell(x, y, value)
                row_cells.append(cell)
            grid.append(row_cells)
        self.grid = grid

    def get_cell(self) -> Cell:
        pass


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    #Niveau 1
    grid1 = Grid(
        width=config.levels[0].width,
        height=config.levels[0].height,
        seed=config.seed
    )
    #Niveau 2
    grid2 = Grid(
        width=config.levels[0].width,
        height=config.levels[0].height,
        seed=None
    )