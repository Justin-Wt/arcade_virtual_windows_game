# Made in 04 May-Now
# Time: 5hr
import arcade
import os
from floating_icon import icon_maker
from wallpaper_Menu import WallpaperWindow
from lesson11 import StartScreen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
width = 19206
height = 1080
title = "Window"


class windows(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
        self.icon_maker = icon_maker(self.width, self.height)
        self.game = StartScreen()
        self.wallpaper_windows = WallpaperWindow(
            self.width // 2,
            self.width // 2,
            self.width * 2 // 3,
            self.height * 2 // 3,
            "Wallpaper",
        )
        self.icons = []
        self.bg = arcade.load_texture(
            os.path.join(BASE_DIR, "assets", "UI's", "Background.png")
        )
        self.photoshop_icon = arcade.load_texture(
            os.path.join(BASE_DIR, "assets", "UI's", "Wallpaper_Icon.png")
        )
        self.photoshop_text = arcade.Text(
            "Wallpaper", 10, self.height - 100, arcade.color.WHITE, font_size=14
        )

    def setup(self):
        self.set_mouse_visible(True)
        self.icon_maker.icon = 0
        data = self.icon_maker.create_icon("Wallpaper_Icon", "Wallpaper")
        self.icons = [
            {
                "image": "Wallpaper_Icon",
                "name": "Wallpaper",
                "clicked": False,
                "hover": False,
                "index": 0,
                "enter": False,
                "goto": self.wallpaper_windows,
                **data,
            }
        ]

    def on_draw(self):
        self.clear()
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
                    arcade.XYWH(x, y, w + 22, h + 27), (0, 0, 255, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 20, h + 25), (255, 255, 255, 200)
                )
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 20, h + 20), (0, 0, 139, 0)
                )
            if icon["hover"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 22, h + 27), (0, 0, 255, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 20, h + 25), (255, 255, 255, 200)
                )
            arcade.draw_texture_rect(icon["texture"], arcade.XYWH(x, y, w, h))
            icon["text"].draw()

        arcade.draw_rect_filled(
            arcade.XYWH(self.width // 2, 20, self.width, 40), arcade.color.DARK_GRAY
        )

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
                    icon["goto"]()
                    icon["clicked"] = False
                else:
                    icon["clicked"] = True
            elif (
                not ((left <= x <= right) and (bottom <= y <= up))
                and icon["clicked"] == True
            ):
                icon["clicked"] = False


def good():
    print("Letsgoo")


window = windows(width, height, title)
window.setup()
arcade.run()
