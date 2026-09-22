# PACMAN - 42Luxembourg 2026 - kmalfois

from pathlib import Path
from src.data_lib import Movements as Mvt
from src.entity import Ghost, Gs
from src.entity import Pacman


class SpriteManager:
    def __init__(self) -> None:
        self.assets_dir: Path = Path("assets/sprites")
        self.pacman_dir: Path = self.assets_dir / "pacman"
        self.blinky_dir: Path = self.assets_dir / "blinky"
        self.pinky_dir: Path = self.assets_dir / "pinky"
        self.inky_dir: Path = self.assets_dir / "inky"
        self.clyde_dir: Path = self.assets_dir / "clyde"
        self.eyes_dir: Path = self.assets_dir / "eyes"
        self.pacman: list[str] = [
            "p1.png", "p2.png",
            "p3.png", "p4.png",
            "pu1.png", "pu2.png",
            "pu3.png", "pu4.png",
        ]
        self.ghost: list[str] = [
            "down1.png", "down2.png",
            "up1.png", "up2.png",
            "left1.png", "left2.png",
            "right1.png", "right2.png",
            "fear1.png", "fear2.png",
            "sleep.png", "wake.png"
        ]
        self.eyes: list[str] = [
            "down.png", "up.png",
            "left.png", "right.png",
        ]

    def get_ghost_sprites(self, ghost: Ghost) -> list[Path]:
        x: int = 0
        y: int = 0
        ghost_folder: Path = Path()

        match type(ghost).__name__:
            case "Blinky": ghost_folder = self.blinky_dir
            case "Pinky": ghost_folder = self.pinky_dir
            case "Inky": ghost_folder = self.inky_dir
            case "Clyde": ghost_folder = self.clyde_dir

        if ghost.state == Gs.FRIGHTENED:
            x, y = 8, 9
        elif ghost.state == Gs.EATEN and not ghost.spawn_snapped:
            match ghost.direction:
                case Mvt.DOWN: return [self.eyes_dir / self.eyes[0]]
                case Mvt.UP: return [self.eyes_dir / self.eyes[1]]
                case Mvt.LEFT: return [self.eyes_dir / self.eyes[2]]
                case Mvt.RIGHT: return [self.eyes_dir / self.eyes[3]]
        elif ghost.state == Gs.EATEN and ghost.spawn_snapped:
            x, y = 10, 11
        else:
            match ghost.direction:
                case Mvt.DOWN: x, y = 0, 1
                case Mvt.UP: x, y = 2, 3
                case Mvt.LEFT: x, y = 4, 5
                case Mvt.RIGHT: x, y = 6, 7

        return [ghost_folder / self.ghost[x], ghost_folder / self.ghost[y]]

    def get_pacman_sprites(self, pacman: Pacman) -> list[Path]:
        if pacman.is_powered_up:
            return [self.pacman_dir / self.pacman[x] for x in range(4, 8)]
        return [self.pacman_dir / self.pacman[x] for x in range(0, 4)]

    def temp_get_wake(self, ghost: Ghost) -> Path:
        ghost_name = type(ghost).__name__.lower()
        folder = getattr(self, f"{ghost_name}_dir", self.blinky_dir)
        return folder / "wake.png"

