.PHONY: run debug install sync clean fclean lint lint-strict

PC = python3

run:
	uv run $(PC) pac-man.py data/configuration.json

debug:
	uv run $(PC) -m pdb pac-man.py data/configuration.json

install:
	uv sync

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

dclean:
	rm -rf build
	rm -rf dist
	rm -rf pacman.spec

fclean: clean dclean
	rm -rf .venv

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

package:
	rm -rf build
	rm -rf dist
	uv run pyinstaller --windowed --clean --name pacman src/__main__.py
	cp -r assets dist/pacman/
	cp -r data dist/pacman/
	cd dist && zip -r pacman.zip pacman/
