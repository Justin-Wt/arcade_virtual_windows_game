# Made in 04 May-Now
# Time: 7hr
import arcade
import os
from floating_icon import icon_maker
import bridge
import json

sAVE_FILE = "Wallpaper.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
width = 1536
height = 864
title = "arcade_virtual_windows_game"


def load_wallpaper():
    with open(sAVE_FILE, "r") as f:
        return json.load(f)


class windows(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
        self.icon_maker = icon_maker(self.width, self.height)
        self.icons = []
        self.total_frames = 0
        self.current_frame = 0
        self.wall = None
        self.frames = None
        self.update_timer = 0
        self.animation_timer = 0
        self.photoshop_icon = arcade.load_texture(
            os.path.join(BASE_DIR, "assets", "UI's", "Wallpaper_Icon.png")
        )
        self.photoshop_text = arcade.Text(
            "Wallpaper", 10, self.height - 100, arcade.color.WHITE, font_size=14
        )

    def setup(self):
        self.set_mouse_visible(True)
        wallpaper_data = load_wallpaper()
        self.wall = wallpaper_data.get("Bg")
        self.total_frames = wallpaper_data.get("frame")
        self.frames = self.load_wallpaper_sprite()
        self.icon_maker.icon = 0
        wallpaper = self.icon_maker.UI_Maker("Wallpaper_Icon", "Wallpaper")
        wallpaper["goto"] = "wallpaper_Menu"
        rpg_game = self.icon_maker.UI_Maker("rpg_game_Icon", "Rpg")
        rpg_game["goto"] = "lesson11"
        ChatJt = self.icon_maker.UI_Maker("ChatJt_Icon", "ChatJt")
        ChatJt["goto"] = "ChatBot_Interface"
        Multi_Emulator = self.icon_maker.UI_Maker(
            "Multi_Emulator_Icon", "Multi", "Emulator"
        )
        Multi_Emulator["goto"] = "Multi_Emulator"
        self.icons = (wallpaper, rpg_game, Multi_Emulator, ChatJt)

    def load_wallpaper_sprite(self):
        frames = []
        for i in range(self.total_frames):
            bg = arcade.load_texture(
                os.path.join(
                    BASE_DIR,
                    "assets",
                    "UI's",
                    "Backgrounds",
                    self.wall,
                    f"{self.wall}{i}.png",
                )
            )
            frames.append(bg)
        return frames

    def on_draw(self):
        self.clear()
        self.bg = self.frames[self.current_frame]
        arcade.draw_texture_rect(
            self.bg,
            arcade.XYWH(
                self.width // 2,
                self.height // 2,
                self.width,
                self.height,
            ),
        )
        for icon in self.icons:
            x, y, w, h = icon["rect"]
            if icon["clicked"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y - 10, w + 22, h + 32), (0, 0, 255, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y - 10, w + 20, h + 30), (255, 255, 255, 200)
                )
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 20, h + 20), (0, 0, 139, 0)
                )
            if icon["hover"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y - 10, w + 22, h + 32), (0, 0, 255, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y - 10, w + 20, h + 30), (255, 255, 255, 200)
                )
            arcade.draw_texture_rect(icon["texture"], arcade.XYWH(x, y, w, h))
            for text in icon["text"]:
                text.draw()

        arcade.draw_rect_filled(
            arcade.XYWH(self.width // 2, 20, self.width, 40), arcade.color.DARK_GRAY
        )

    def on_update(self, delta_time):
        # Animate frames
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= self.total_frames:
                self.current_frame = 0

        # Check wallpaper.json every second
        self.update_timer += delta_time
        if self.update_timer >= 1:
            self.update_timer = 0
            wallpaper_data = load_wallpaper()
            new_wall = wallpaper_data.get("Bg")
            new_total = wallpaper_data.get("frame")
            # Reload ONLY if changed
            if new_wall != self.wall or new_total != self.total_frames:
                self.wall = new_wall
                self.total_frames = new_total
                self.frames = self.load_wallpaper_sprite()
                self.current_frame = 0

    def on_mouse_motion(self, x, y, dx, dy):
        for icon in self.icons:
            rx, ry, rw, rh = icon["rect"]
            left = rx - rw / 2
            right = rx + rw / 2
            bottom = ry - rh / 2
            up = ry + rh / 2
            if (left <= x <= right) and (bottom <= y <= up):
                icon["hover"] = True
            else:
                icon["hover"] = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        for icon in self.icons:
            rx, ry, rw, rh = icon["rect"]
            left = rx - rw / 2
            right = rx + rw / 2
            bottom = ry - rh / 2
            up = ry + rh / 2
            if (left <= x <= right) and (bottom <= y <= up):
                if icon["clicked"] == True:
                    print(icon["goto"])
                    bridge.open_window(icon["goto"])
                    icon["clicked"] = False
                else:
                    icon["clicked"] = True
            elif (
                not ((left <= x <= right) and (bottom <= y <= up))
                and icon["clicked"] == True
            ):
                icon["clicked"] = False


window = windows(width, height, title)
window.setup()
arcade.run()
