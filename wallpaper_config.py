import arcade
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
speed = 5
update_frame = 5

right = 0
left = 1


def load_texture_pair(filename):
    return arcade.load_texture(filename)


class Wallpaper(arcade.Sprite):
    def __init__(self, path, frames):
        super().__init__()

        self.char_face_dir = right

        self.cur_texture = 0

        self.scale = 0.8

        # adjust the collision box
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # load textures
        main_path = os.path.join(BASE_DIR, "assets", "UI's", path, path)
        # load textures for idle
        self.wallpaper = []
        for i in range(frames):
            self.texture = load_texture_pair(f"{main_path}.png")
            self.wallpaper.append(self.texture)

    def update_animation(self, delta_time=1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 7 * update_frame:
            self.cur_texture = 0
        frame = self.cur_texture // update_frame
        self.texture = self.wallpaper[frame]
