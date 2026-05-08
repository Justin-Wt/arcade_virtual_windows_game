import arcade
from pathlib import Path  # import path from pathlib
from players import PlayerChar
import random
import noise  # NEW
import math
import subprocess  # NEW
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
screen_width, screen_height = arcade.get_display_size()
CHUNK_SIZE = 8
TILE_SIZE = 70
speed = 5
fontsize = 40 / 70
coin_scale = 0.5
path = Path(__file__).parent  # faster load handles for files
title = "Making Infinite Map"


def smooth_noise(x, y):
    return (
        math.sin(x * 0.05 + y * 0.03)
        + math.cos(y * 0.05 - x * 0.02)
        + math.sin((x + y) * 0.02)
    )


def get_tile(x, y):
    random.seed(x * 10000 + y)
    r = smooth_noise(x, y)
    if r < 0.2:
        return "water"
    elif r < 0.5:
        return "stone"
    else:
        return "grass"


def generate_chunk(cx, cy):
    sprite_list = arcade.SpriteList()
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            world_x = cx * CHUNK_SIZE + x
            world_y = cy * CHUNK_SIZE + y
            tile = get_tile(world_x, world_y)
            sprite = arcade.Sprite(
                os.path.join(BASE_DIR, "assets", "tiles", f"{tile}.png"), scale=1
            )
            sprite.center_x = world_x * TILE_SIZE
            sprite.center_y = world_y * TILE_SIZE
            sprite_list.append(sprite)
    return sprite_list


class game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.right_pressed = False
        self.left_pressed = False
        self.back_pressed = False
        self.front_pressed = False

    def setup(self):
        self.camera = arcade.Camera2D()
        self.players = arcade.SpriteList()
        self.player = PlayerChar()
        self.players.append(self.player)
        self.player.center_x = 0
        self.player.center_y = 0
        self.player_speed = 5
        self.loaded_chunks = {}
        self.VISIBLE_RADIUS = 2

    def on_draw(self):
        self.clear()
        self.camera.use()
        for chunk in self.loaded_chunks.values():
            chunk.draw()
        self.players.draw()

    def on_update(self, delta_time):
        self.player.update()
        if self.left_pressed:
            self.players.update_animation("Left")
        elif self.right_pressed:
            self.players.update_animation("Right")
        elif self.back_pressed:
            self.players.update_animation("Back")
        elif self.front_pressed:
            self.players.update_animation("Front")
        else:
            self.players.update_animation()
        self.camera.position = (self.player.center_x, self.player.center_y)
        player_chunk_x = int(self.player.center_x // (TILE_SIZE * CHUNK_SIZE))
        player_chunk_y = int(self.player.center_y // (TILE_SIZE * CHUNK_SIZE))
        for cx in range(
            player_chunk_x - self.VISIBLE_RADIUS,
            player_chunk_x + self.VISIBLE_RADIUS + 1,
        ):
            for cy in range(
                player_chunk_y - self.VISIBLE_RADIUS,
                player_chunk_y + self.VISIBLE_RADIUS + 1,
            ):
                if (cx, cy) not in self.loaded_chunks:
                    self.loaded_chunks[(cx, cy)] = generate_chunk(cx, cy)
        for cx, cy in list(self.loaded_chunks):
            if (
                abs(cx - player_chunk_x) > self.VISIBLE_RADIUS
                or abs(cy - player_chunk_y) > self.VISIBLE_RADIUS
            ):
                del self.loaded_chunks[(cx, cy)]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            if modifiers & arcade.key.MOD_SHIFT:
                self.player.change_x = -self.player_speed * 2
                self.left_pressed = True
                self.right_pressed = False
            else:
                self.player.change_x = -self.player_speed
                self.left_pressed = True
                self.right_pressed = False

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if modifiers & arcade.key.MOD_SHIFT:
                self.player.change_x = self.player_speed * 2
                self.left_pressed = False
                self.right_pressed = True
            else:
                self.player.change_x = self.player_speed
                self.left_pressed = False
                self.right_pressed = True

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player.change_y = self.player_speed
            self.back_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -self.player_speed
            self.front_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.MOD_SHIFT:
            self.player_speed = 5
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0
            self.right_pressed = False
            self.left_pressed = False
        if key in (
            arcade.key.SPACE,
            arcade.key.W,
            arcade.key.S,
            arcade.key.UP,
            arcade.key.DOWN,
        ):
            self.player.change_y = 0
            self.front_pressed = False
            self.back_pressed = False


def spawn_popup():
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "popup.py")])


def spawn_skill_menu():
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "skill_menu.py")])


if __name__ == "__main__":
    with open(os.path.join(BASE_DIR, "assets", "json", "error_count.json"), "w") as f:
        f.write("0")
    window = game(screen_width, screen_height, title)
    window.setup()
    arcade.run()
