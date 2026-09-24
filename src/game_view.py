from src.config import GameConfig, load_config
from src.grid.grid_loader import Grid
from src.grid.cell import StateType
from src.end_view import EndView
from src.data_lib import Movements
from src.entity_manager import EntityManager
from src.sprite_manager import SpriteManager
from src import entity

import arcade


class GameView(arcade.View):
    def __init__(self, config: GameConfig):
        super().__init__()
        self.config = config
        self.current_level = 1
        self.start = False
        self.is_all_empty = False
        self.pause = False
        self.cheat_mode = False
        self.invincible = False
        self.ghost_freeze = False
        self.lives = config.lives
        self.options = ["RESUME", "MAIN MENU"]
        self.selected = 0
        self.score = 0

        self.animation_timer = 0.0
        self.sprite_manager = SpriteManager()
        self.ghost_sprites: arcade.SpriteList = arcade.SpriteList()
        self.ghost_sprite_map: dict[int, arcade.Sprite] = {}
        self.pacman_sprite_list: arcade.SpriteList = arcade.SpriteList()
        self.pacman_sprite: arcade.Sprite | None = None

        self.load_level()

    def calculate_render_params(self):
        cell_size_w = (self.window.width * 0.6) / self.grid.width
        cell_size_h = (self.window.height * 0.6) / self.grid.height
        self.cell_size = min(cell_size_w, cell_size_h)
        self.offset_x = (self.window.width - self.grid.width * self.cell_size) / 2
        self.offset_y = (self.window.height - self.grid.height * self.cell_size) / 2

    def load_level(self):
        level_config = self.config.levels[self.current_level - 1]
        seed = self.config.seed if self.current_level == 1 else None
        self.grid = Grid(
            level_config.width,
            level_config.height,
            seed
        )
        self.grid.place_items(self.config.pacgum)
        self.entity_manager = EntityManager(self.grid, base_speed=5.0)
        self.entity_manager.pacman.is_invincible = self.invincible
        self.entity_manager.ghost_freeze = self.ghost_freeze
        self.time_left = self.config.level_max_time
        self.start = False
        self.calculate_render_params()
        self.setup_sprites()

    def next_level(self):
        self.current_level += 1
        if self.current_level > len(self.config.levels):
            self.window.show_view(EndView(self.score, self.config, True))
            return
        self.load_level()

    def on_draw(self):
        self.clear()
        self.draw_maze()
        self.draw_items()
        self.draw_token()
        self.draw_hud()
        self.draw_page()
        if self.pause:
            self.draw_pause_menu()
        if self.cheat_mode:
            self.draw_cheat_panel()

    def draw_maze(self):
        for row in self.grid.grid:
            for cell in row:
                px = self.offset_x + cell.x * self.cell_size
                py = self.offset_y + (self.grid.height - 1 - cell.y) * self.cell_size
                if not any([cell.north, cell.east, cell.south, cell.west]):
                    arcade.draw_lbwh_rectangle_filled(
                        px,
                        py,
                        self.cell_size,
                        self.cell_size,
                        arcade.color.BLUE
                    )
                if not cell.north:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px + self.cell_size,
                        py + self.cell_size,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.east:
                    arcade.draw_line(
                        px + self.cell_size,
                        py + self.cell_size,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.south:
                    arcade.draw_line(
                        px,
                        py,
                        px + self.cell_size,
                        py,
                        arcade.color.WHITE,
                        1
                    )
                if not cell.west:
                    arcade.draw_line(
                        px,
                        py + self.cell_size,
                        px,
                        py,
                        arcade.color.WHITE,
                        1
                    )

    def draw_items(self):
        for row in self.grid.grid:
            for cell in row:
                px = self.offset_x + cell.x * self.cell_size
                py = self.offset_y + (self.grid.height - 1 - cell.y) * self.cell_size
                center_x = px + self.cell_size / 2
                center_y = py + self.cell_size / 2
                if cell.state_type == StateType.SUPER_PACGUM:
                    arcade.draw_circle_filled(
                        center_x,
                        center_y,
                        self.cell_size * 0.25,
                        arcade.color.PINK
                    )
                elif cell.state_type == StateType.PACGUM:
                    arcade.draw_circle_filled(
                        center_x,
                        center_y,
                        self.cell_size * 0.15,
                        arcade.color.YELLOW
                    )

    def draw_token(self):
        # 0. Calculate animation frame index (toggles between 0 and 1 at ~8 FPS)
        frame_idx = 0 if int(self.animation_timer * 8) % 2 == 0 else 1

        # 1. Update and Draw Pac-Man
        pacman = self.entity_manager.pacman
        pac_center_x = self.offset_x + pacman.x * self.cell_size
        pac_center_y = self.offset_y + (self.grid.height - pacman.y) * self.cell_size

        if self.pacman_sprite:
            pac_textures = self.sprite_manager.get_pacman_sprites(pacman)
            # Cycle through Pac-Man's 3 mouth frames
            pac_frame_idx = int(self.animation_timer * 12) % len(pac_textures)
            self.pacman_sprite.texture = pac_textures[pac_frame_idx]

            self.pacman_sprite.center_x = pac_center_x
            self.pacman_sprite.center_y = pac_center_y
            self.pacman_sprite_list.draw()
        else:
            arcade.draw_circle_filled(
                pac_center_x,
                pac_center_y,
                self.cell_size * 0.4,
                arcade.color.YELLOW
            )

        # 2. Update Ghost Sprites
        frighten_timer = self.entity_manager.frighten_timer
        is_frightened = self.entity_manager.current_behavior == entity.Gs.FRIGHTENED

        for ghost in self.entity_manager.ghosts:
            ghost_sprite = self.ghost_sprite_map.get(id(ghost))
            if ghost_sprite:
                ghost_textures = self.sprite_manager.get_ghost_sprites(ghost)
                ghost_sprite.center_x = self.offset_x + ghost.x * self.cell_size
                ghost_sprite.center_y = self.offset_y + (self.grid.height - ghost.y) * self.cell_size

                # EATEN & SLEEPING AT SPAWN
                if ghost.state == entity.Gs.EATEN and ghost.spawn_snapped:
                    # While respawn_timer counts down from 5.0 to 0.0:
                    if ghost.respawn_timer > 2.0:
                        # First 3 seconds: static sleeping frame
                        selected_idx = 0
                    else:
                        # Final 2 seconds: alternate/flash frames at ~8 FPS
                        selected_idx = 0 if int(self.animation_timer * 8) % 2 == 0 else 1

                # STANDARD (CHASE / SCATTER / EATEN RETURNING EYES)
                else:
                    selected_idx = frame_idx if len(ghost_textures) > 1 else 0

                # Bounds guard in case a state list only returns 1 texture
                if selected_idx >= len(ghost_textures):
                    selected_idx = 0

                ghost_sprite.texture = ghost_textures[selected_idx]

        self.ghost_sprites.draw()

    def draw_cheat_panel(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )
        cheat = [
            f"[I] Invincible: {'ON' if self.invincible else 'OFF'}",
            "[N] Skip Level",
            f"[F] Freeze Ghosts: {'ON' if self.ghost_freeze else 'OFF'}",
            f"[L] Add Life ({self.lives})"
        ]
        for i, text in enumerate(cheat):
            arcade.draw_text(
                text,
                self.window.width / 2,
                self.window.height / 2 + 50 - i * 80,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                bold=True
            )

    def draw_hud(self):
        arcade.draw_text(
            "❤️" * self.lives,
            self.window.width / 10,
            self.window.height - 30,
            arcade.color.RED,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"LEVEL: {self.current_level}",
            self.window.width / 10 * 3,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"SCORE: {self.score}",
            self.window.width / 10 * 6,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            f"TIMER: {int(self.time_left)}",
            self.window.width / 10 * 9,
            self.window.height - 30,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def draw_pause_menu(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = arcade.color.BLUE
                prefix = ">"
            else:
                color = arcade.color.WHITE
                prefix = " "
            arcade.draw_text(
                prefix + option,
                self.window.width / 2,
                self.window.height * 0.85 - 200 if i == 0 else self.window.height * 0.85 - 400,
                color,
                24,
                anchor_x="center",
                bold=True
            )

    def draw_page(self):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            self.window.width,
            60,
            arcade.color.ORANGE
        )
        arcade.draw_text(
            "DIRECTIONS: ↑ ↓ ← →",
            self.window.width / 4,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )
        arcade.draw_text(
            "PAUSE: P",
            self.window.width / 4 * 2,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )
        arcade.draw_text(
            "CHEAT MODE: C",
            self.window.width / 4 * 3,
            30,
            arcade.color.BLACK,
            15,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        # pause menu
        if key == arcade.key.P:
            self.pause = not self.pause
            return

        if self.pause:
            if key == arcade.key.UP:
                self.selected = 0
            elif key == arcade.key.DOWN:
                self.selected = 1
            elif key == arcade.key.ENTER:
                if self.selected == 0:
                    self.pause = not self.pause
                elif self.selected == 1:
                    from src.main_menu import MainMenuView
                    menu = MainMenuView(load_config("data/configuration.json"))
                    self.window.show_view(menu)
            return

        # cheat mode
        if key == arcade.key.C:
            self.cheat_mode = not self.cheat_mode
            return

        if self.cheat_mode:
            if key == arcade.key.I:
                self.invincible = not self.invincible
                self.entity_manager.pacman.is_invincible = self.invincible
            elif key == arcade.key.N:
                if self.current_level < len(self.config.levels):
                    self.next_level()
            elif key == arcade.key.F:
                self.ghost_freeze = not self.ghost_freeze
                self.entity_manager.ghost_freeze = self.ghost_freeze
            elif key == arcade.key.L:
                self.lives += 1
            return

        # pacman move
        if key == arcade.key.UP:
            self.start = True
            self.entity_manager.pacman.buffered_direction = Movements.UP
        elif key == arcade.key.DOWN:
            self.start = True
            self.entity_manager.pacman.buffered_direction = Movements.DOWN
        elif key == arcade.key.LEFT:
            self.start = True
            self.entity_manager.pacman.buffered_direction = Movements.LEFT
        elif key == arcade.key.RIGHT:
            self.start = True
            self.entity_manager.pacman.buffered_direction = Movements.RIGHT

    def on_update(self, delta_time):
        if self.pause or self.cheat_mode or not self.start:
            return
        dt = min(delta_time, 1 / 30.0)
        self.animation_timer += dt
        if self.start:
            self.time_left -= dt
        summary = self.entity_manager.update(dt)
        if summary.eat_pacgum:
            self.score += self.config.points_per_pacgum
        if summary.eat_superpacgum:
            self.score += self.config.points_per_super_pacgum
        if summary.eaten_ghosts:
            count = len(summary.eaten_ghosts)
            self.score += self.config.points_per_ghost * count
        if summary.defeated:
            self.lives -= 1
            self.start = False
            if self.lives <= 0:
                self.window.show_view(EndView(self.score, self.config, False))
                return
            self.entity_manager.reset_positions()
            self.entity_manager.pacman.active = True
            self.entity_manager.pacman.direction = None
            self.entity_manager.set_ghost_states(entity.Gs.SCATTER)
        if self.grid.is_all_empty():
            self.next_level()
            if self.current_level > len(self.config.levels):
                self.window.show_view(EndView(self.score, self.config, True))
        if self.time_left <= 0:
            self.window.show_view(EndView(self.score, self.config, False))

    def setup_sprites(self) -> None:
        """Creates Arcade sprites using pre-loaded textures from SpriteManager."""
        self.pacman_sprite_list.clear()
        self.ghost_sprites.clear()
        self.ghost_sprite_map.clear()

        pacman = self.entity_manager.pacman
        pac_textures = self.sprite_manager.get_pacman_sprites(pacman)

        # Pass pac_textures[0] directly as a positional argument:
        self.pacman_sprite = arcade.Sprite(pac_textures[0])

        base_dim = max(self.pacman_sprite.texture.width, self.pacman_sprite.texture.height)
        self.pacman_sprite.scale = (self.cell_size * 0.8) / base_dim
        self.pacman_sprite.center_x = self.offset_x + pacman.x * self.cell_size
        self.pacman_sprite.center_y = self.offset_y + (self.grid.height - pacman.y) * self.cell_size
        self.pacman_sprite_list.append(self.pacman_sprite)

        for ghost in self.entity_manager.ghosts:
            ghost_textures = self.sprite_manager.get_ghost_sprites(ghost)

            # Pass ghost_textures[0] directly as a positional argument:
            ghost_sprite = arcade.Sprite(ghost_textures[0])

            base_dim = max(ghost_sprite.texture.width, ghost_sprite.texture.height)
            ghost_sprite.scale = (self.cell_size * 0.8) / base_dim
            ghost_sprite.center_x = self.offset_x + ghost.x * self.cell_size
            ghost_sprite.center_y = self.offset_y + (self.grid.height - ghost.y) * self.cell_size
            self.ghost_sprite_map[id(ghost)] = ghost_sprite
            self.ghost_sprites.append(ghost_sprite)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.calculate_render_params()
        for ghost_sprite in self.ghost_sprites:
            base_dim = max(ghost_sprite.texture.width, ghost_sprite.texture.height)
            ghost_sprite.scale = (self.cell_size * 0.8) / base_dim
        if self.pacman_sprite:
            base_dim = max(self.pacman_sprite.texture.width, self.pacman_sprite.texture.height)
            self.pacman_sprite.scale = (self.cell_size * 0.8) / base_dim


if __name__ == "__main__":
    config = load_config("data/configuration.json")
    screen_width, screen_height = arcade.get_display_size()
    window = arcade.Window(int(screen_width * 0.95), int(screen_height * 0.95), "PAC-MAN Test")
    view = GameView(config)
    window.show_view(view)
    arcade.run()
