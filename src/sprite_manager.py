# PACMAN - 42Luxembourg 2026 - kmalfois

from pathlib import Path
import arcade


from src.data_lib import Movements as Mvt
from src.entity import Ghost, Gs, Pacman


class SpriteManager:
    """Load and select sprites for Pac-Man and ghosts.

    Attributes:
        assets_dir: Root directory containing the sprite assets.
        ghost_textures: Textures indexed by ghost name and movement state.
        eyes_textures: Ghost eye textures indexed by movement direction.
        pacman_textures: Pac-Man animation frames indexed by direction.
        pacman_last_direction: Most recent direction used by Pac-Man.
    """

    def __init__(self) -> None:
        """Initialize sprite storage and load all game textures."""
        self.assets_dir: Path = Path("assets/sprites")
        self.ghost_textures: dict[str, dict[Mvt | str, list[arcade.Texture]]] = {}
        self._load_ghost_textures()
        self.eyes_textures: dict[Mvt, arcade.Texture] = {}
        self._load_eyes_textures()
        self.pacman_textures: dict[Mvt, list[arcade.Texture]] = {}
        self.pacman_last_direction: Mvt | None = None
        self._load_pacman_textures()

    def _load_ghost_textures(self) -> None:
        """Load directional, frightened, and respawn ghost textures."""
        for ghost in ["blinky", "pinky", "inky", "clyde"]:
            folder: Path = self.assets_dir / ghost
            self.ghost_textures[ghost] = {
                Mvt.UP: [
                    arcade.load_texture(folder / "up1.png"),
                    arcade.load_texture(folder / "up2.png")
                ],
                Mvt.LEFT: [
                    arcade.load_texture(folder / "left1.png"),
                    arcade.load_texture(folder / "left2.png")
                ],
                Mvt.RIGHT: [
                    arcade.load_texture(folder / "right1.png"),
                    arcade.load_texture(folder / "right2.png")
                ],
                Mvt.DOWN: [
                    arcade.load_texture(folder / "down1.png"),
                    arcade.load_texture(folder / "down2.png")
                ],
                "frightened": [
                    arcade.load_texture(folder / "fear1.png"),
                    arcade.load_texture(folder / "fear2.png")
                ],
                "respawn": [
                    arcade.load_texture(folder / "sleep.png"),
                    arcade.load_texture(folder / "wake.png")
                ]
            }

    def _load_eyes_textures(self) -> None:
        """Load ghost eye textures for each movement direction."""
        folder = self.assets_dir / "eyes"
        for direction in Mvt:
            self.eyes_textures[direction] = arcade.load_texture(folder / f"{direction.value.lower()}.png")

    def _load_pacman_textures(self) -> None:
        """Load Pac-Man animation frames for each movement direction."""
        folder = self.assets_dir / "pacman"
        for direction in Mvt:
            self.pacman_textures[direction] = [
                arcade.load_texture(folder / f"{direction.value.lower()}1.png"),
                arcade.load_texture(folder / f"{direction.value.lower()}2.png"),
                arcade.load_texture(folder / f"{direction.value.lower()}3.png")
            ]

    def get_ghost_sprites(self, ghost: Ghost) -> list[arcade.Texture]:
        """Return the textures appropriate for a ghost's current state.

        Args:
            ghost: Ghost whose current state and direction determine the sprites.

        Returns:
            A list containing the ghost animation frames or eye texture.
        """
        ghost_name = type(ghost).__name__.lower()
        if ghost.state == Gs.FRIGHTENED:
            return self.ghost_textures[ghost_name]["frightened"]
        elif ghost.state == Gs.EATEN:
            if ghost.spawn_snapped:
                return self.ghost_textures[ghost_name]["respawn"]
            direction = ghost.direction if isinstance(ghost.direction, Mvt) else Mvt.LEFT
            return [self.eyes_textures[direction]]
        elif ghost.direction:
            return self.ghost_textures[ghost_name][ghost.direction]
        else:
            return [self.ghost_textures[ghost_name]["respawn"][1]]

    def get_pacman_sprites(self, pacman: Pacman) -> list[arcade.Texture]:
        """Return the animation frames appropriate for Pac-Man's direction.

        Args:
            pacman: Pac-Man entity whose direction determines the sprites.

        Returns:
            Pac-Man animation frames, or a fallback frame when stationary.
        """
        if pacman.direction:
            self.pacman_last_direction = pacman.direction
            return self.pacman_textures[pacman.direction]
        if self.pacman_last_direction:
            return [self.pacman_textures[self.pacman_last_direction][1]]
        return [self.pacman_textures[Mvt.LEFT][0]]
