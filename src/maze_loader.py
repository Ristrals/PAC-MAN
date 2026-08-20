from mazegenerator import MazeGenerator
from src.config import load_config
from src.cell import Cell, create_cell


def maze_load(width: int, height: int, seed: int) -> list[Cell]:
    try:
        m = MazeGenerator(size=(width, height), perfect=False)
        m.generate(seed=seed)
    except Exception as e:
        print(f"Error: maze generation is failed, {e}")
        return []
    if not m.maze:
        print("Error: maze data is empty")
        return []
    cells: list[Cell] = []
    for y, row in enumerate(m.maze):
        for x, value in enumerate(row):
            cell = create_cell(x, y, value)
            cells.append(cell)
    return cells


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    cells = maze_load(
        width=config.levels[0].width,
        height=config.levels[0].height,
        seed=config.seed
    )
