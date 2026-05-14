# 6 hrs
import math
import arcade
from threed_shape_maker import ThreeD_Cube
import random
import trimesh

WIDTH = 1280
HEIGHT = 720


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade 3D")
        arcade.set_background_color(arcade.color.BLACK)
        self.cube = []
        for i in range(1, 9):
            for j in range(1, 9):
                cube = ThreeD_Cube(
                    i,
                    1,
                    j,
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    ),
                )
                self.cube.append(cube)
        self.up_rotation = 0
        self.side_rotation = 0
        self.up_moves = 0
        self.left_moves = 0
        self.walk = 10

    def project(self, x, y, z):
        distance = 5
        scale = 400
        z += distance
        factor = scale / z
        screen_x = x * factor + WIDTH // 2
        screen_y = y * factor + HEIGHT // 2
        return screen_x, screen_y

    def on_draw(self):
        self.clear()
        all_faces = []
        all_lines = []
        for cube in self.cube:
            cube_color, cube_outline = cube.draw_cube(
                WIDTH,
                HEIGHT,
                self.up_rotation,
                self.side_rotation,
                self.walk,
                self.up_moves,
                self.left_moves,
            )
            all_faces.extend(cube_color)
            all_lines.extend(cube_outline)
        all_faces.sort(key=lambda item: item[0], reverse=True)
        for x1, y1, x2, y2, color, width in all_lines:
            arcade.draw_line(x1, y1, x2, y2, color, width)
        for _, points, color in all_faces:
            arcade.draw_polygon_filled(points, color)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            self.up_rotation += dy * 0.01
            self.side_rotation -= dx * 0.01
        elif buttons & arcade.MOUSE_BUTTON_RIGHT:
            self.up_moves += dy * 1
            self.left_moves += dx * 1

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.walk -= scroll_y * 0.5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.walk -= 0.5
        elif key == arcade.key.S:
            self.walk += 0.5
        if key == arcade.key.A:
            self.side_rotation += 0.1
        elif key == arcade.key.D:
            self.side_rotation -= 0.1


window = Game()
arcade.run()
