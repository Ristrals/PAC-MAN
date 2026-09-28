.PHONY: run debug install sync clean fclean lint lint-strict

PC = python3

run:
	uv run $(PC) -m src data/configuration.json

debug:
	uv run $(PC) -m pdb -m src data/configuration.json

install:
	uv sync

dist:
	python -m PyInstaller pacman_game.spec --clean

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

dclean:
	rm -rf dist
	rm -rf build

fclean: clean
	rm -rf .venv
	rm -rf build
	rm -rf dist

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

mp:
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

f8:
	flake8 .
