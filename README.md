*This project has been created as part of the 42 curriculum by juruan, kmalfois*

-------------------------------------------------------------------------------
PACMAN Project
=============

-------------------------------------------------------------------------------
# DESCRIPTION

This project is a remake of the classic arcade game **Pac-Man**, written in
Python with the [arcade](https://api.arcade.academy/) library.

The player moves Pac-Man through a maze to eat every pacgum while avoiding the
four ghosts (Blinky, Pinky, Inky and Clyde). Eating a super pacgum makes the
ghosts frightened for a short time, so Pac-Man can eat them for extra points.
A level is cleared when every pacgum is eaten. The game ends when the player
loses all their lives or when the level timer runs out.

Main features:
- **Generated mazes**: mazes are built with the `mazegenerator` package. The
  first level uses the seed from the configuration, so it is always the same;
  the next levels are generated randomly.
- **10 levels**: the game has 10 levels and the maze grows with each one.
  The player wins the game after clearing all 10 levels.
- **JSON configuration**: lives, scores, timer, seed and level sizes are read
  from a configuration file and checked with pydantic.
- **Highscores**: the top 10 scores are saved in a JSON file.
- **Main menu**: start the game, show the highscores, or quit the game.
- **Pause menu** (`P`): resume the game or go back to the main menu.
- **Cheat mode** (`C`): makes the game easier:
  - `I`: invincibility (toggle)
  - `F`: freeze the ghosts (toggle)
  - `N`: skip to the next level
  - `L`: get an extra life

-------------------------------------------------------------------------------
# INSTRUCTIONS

## REQUIREMENTS
- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) (Python package manager)

Dependencies (installed automatically by uv, see `pyproject.toml`):
- `arcade`: game window, drawing and keyboard input
- `pydantic`: configuration validation
- `mazegenerator`: maze generation. This package is provided with the
  project as the local wheel `mazegenerator-2.1.0-py3-none-any.whl`. If
  needed, it can be downloaded again from the project page.

## INSTALLATION
```bash
make install
```
This runs `uv sync`, which creates the `.venv` virtual environment
and installs all the dependencies.

## EXECUTION
```bash
make run
```
or, with any configuration file:
```bash
uv run python3 pac-man.py <config.json>
```
The configuration file is required. The default one is
`data/configuration.json`.

## STANDALONE EXECUTABLE
```bash
make package
```
This step is optional: it is only needed to share the game as a program
that runs on its own. It builds the game with
[PyInstaller](https://pyinstaller.org/) in `dist/pacman/` and creates
`dist/pacman.zip`. The executable can be launched without Python or uv
installed, on the same operating system it was built on. It uses `data/configuration.json` by default.

## CONTROLS
| Key | Action |
|-----|--------|
| Arrow keys | Move Pac-Man / navigate menus |
| `Enter` | Confirm a menu choice |
| `P` | Pause / resume |
| `C` | Toggle cheat mode |
| `Esc` | Quit (from the main menu) |

## MAKEFILE
Makefile commands:
- **make install**: Creates the virtual environment and installs the
  dependencies with `uv sync`.
- **make run**: Runs the game with `data/configuration.json`.
- **make debug**: Runs the game with Python's debugger (`pdb`).
- **make clean**: Removes `__pycache__` and `.mypy_cache` directories.
- **make fclean**: Runs `make clean`, then removes the virtual environment
  (`.venv`).
- **make lint**: Runs flake8 and mypy.
- **make lint-strict**: Runs flake8 and mypy with the `--strict` flag.
- **make f8**: Runs flake8 only.
- **make mp**: Runs mypy only.
- **make package**: Builds a standalone executable with PyInstaller in
  `dist/pacman/` (with `assets` and `data`), and zips it into
  `dist/pacman.zip`.

To launch the game without the Makefile:
```bash
uv run python3 pac-man.py data/configuration.json
```

-------------------------------------------------------------------------------
# RESOURCES
- [Arcade documentation](https://api.arcade.academy/): windows, views,
  drawing, sprites and keyboard input.
- [Pydantic documentation](https://docs.pydantic.dev/): models and
  validators used for the configuration file.

-------------------------------------------------------------------------------
# CONFIGURATION

-------------------------------------------------------------------------------
# HIGHSCORE

-------------------------------------------------------------------------------
# MAZE GENERATION

-------------------------------------------------------------------------------
# IMPLEMENTATION

-------------------------------------------------------------------------------
# GENERAL SOFTWARE ARCHITETURE

- **Makefile**: Command file.
- **README.md**: Program guide and information.
- **[assets]**: images used in README.md.
- **[maps]**: map files.
- **[output]**: Simulation's data as JSON file.
- **[src]**: Contains all program files.
 - **__init__.py**: Module init file.
 - **__main__.py**: Module main file.
 - **arbiter.py**: Decision maker.
 - **cogitator.py**: Drone trajectory calculation.
 - **connection.py**: Connection object class.
 - **data_exporter.py**: Data export module.
 - **data_lib.py**: Custom pydantic type library.
 - **drone.py**: Drone object class.
 - **error_handler.py**: Error handler.
 - **hub.py**: Hub object class.
 - **interface.py**: Program interface.
 - **navigator.py**: Map data parsing and extraction.
 - **operator.py**: Orchestrator and simulation runner.
- **[visualizer]**: Contains all visualization files.
  - **simulation_data**.json: JSON result of a simulation.
  - **visualizer.pck**: GoDot file.
  - **visualizer.sh**: GoDot file.
  - **visualizer.x86_64**: Visualizer executable file.
- **.flake8**: Flake8 ignore rules.
- **.gitignore**: Files ignored by git.
- **all_run.py**: Small script to test all available maps
- **.mypy**: mypy directives, excluded files from mypy check
- **pyproject.toml**: Package directives for uv
- **uv.lock**: uv.lock

-------------------------------------------------------------------------------
# PROJECT MANAGEMENT

-------------------------------------------------------------------------------
# PROGRAM

-------------------------------------------------------------------------------
# CODE ARCHITECTURE

-------------------------------------------------------------------------------
# ALGORITHM

-------------------------------------------------------------------------------
# INTERFACE GRAPHIC

-------------------------------------------------------------------------------
# CONCLUSION
LOL

