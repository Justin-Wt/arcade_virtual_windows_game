# Made in 04 May-Now
# Time: 6hr
import arcade
import os
import win32gui
import win32con
from floating_icon import icon_maker
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
width = 1536
height = 864
title = "arcade_virtual_windows_game"
SAVE_FILE = "Wallpaper.json"


def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


class windows(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        hwnd = win32gui.FindWindow(None, title)
        # Set window as topmost
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )
        self.width = width // 2
        self.height = height // 2
        self.icon_maker = icon_maker(self.width, self.height)
        self.icons = []

    def setup(self):
        self.set_mouse_visible(True)
        self.icon_maker.icon = 0
        Default_Wallpaper = self.icon_maker.UI_Maker(
            "Background", "Default", "(Normal Wallpaper)", "Horizontal", 150, 75
        )
        Default_Wallpaper["frames"] = 1
        self.icons.append(Default_Wallpaper)
        Furina_Wallpaper = self.icon_maker.UI_Maker(
            "Furina", "Furina Montagem", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Furina_Wallpaper["frames"] = 181
        self.icons.append(Furina_Wallpaper)
        Shiroko_Wallpaper = self.icon_maker.UI_Maker(
            "Shiroko", "Shiroko x Hoshino", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Shiroko_Wallpaper["frames"] = 204
        self.icons.append(Shiroko_Wallpaper)
        Wuwa_Wallpaper = self.icon_maker.UI_Maker(
            "WutheringWaves",
            "Wuthering Waves",
            "(L2D Wallpaper)",
            "Horizontal",
            150,
            75,
        )
        Wuwa_Wallpaper["frames"] = 158
        self.icons.append(Wuwa_Wallpaper)
        Evernight_Wallpaper = self.icon_maker.UI_Maker(
            "Evernight", "Evernight Dance", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Evernight_Wallpaper["frames"] = 148
        self.icons.append(Evernight_Wallpaper)
        self.icons.append(Furina_Wallpaper)
        Shigure_Wallpaper = self.icon_maker.UI_Maker(
            "Shigure", "Shigure Dance", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Shigure_Wallpaper["frames"] = 149
        self.icons.append(Shigure_Wallpaper)

    def on_draw(self):
        self.clear()
        arcade.draw_rect_filled(
            arcade.XYWH(
                self.width // 2,
                self.height // 2,
                self.width,
                self.height,
            ),
            arcade.color.GRAY,
        )
        for icon in self.icons:
            x, y, w, h = icon["rect"]
            if icon["clicked"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, y - 10, w + 27, h + 32), (0, 0, 0, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, y - 10, w + 25, h + 30), (150, 150, 150, 200)
                )
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, y, w + 20, h + 20), (0, 0, 139, 0)
                )
            if icon["hover"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, y - 10, w + 27, h + 32), (0, 0, 0, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, y - 10, w + 25, h + 30), (150, 150, 150, 200)
                )
            arcade.draw_texture_rect(icon["texture"], arcade.XYWH(x, y, w, h))
            for text in icon["text"]:
                text.draw()

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
                    data = {"Bg": icon["image"], "frame": icon["frames"]}
                    save_data(data)
                    icon["clicked"] = False
                else:
                    icon["clicked"] = True
            elif (
                not ((left <= x <= right) and (bottom <= y <= up))
                and icon["clicked"] == True
            ):
                icon["clicked"] = False


if __name__ == "__main__":
    window = windows(width, height, title)
    window.setup()
    arcade.run()
