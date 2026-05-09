# Made in 04 May-Now
# Time: 6hr
import arcade
import os
import win32gui
import win32con
from floating_icon import icon_maker
import bridge

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
width = 1536
height = 864
title = "arcade_virtual_windows_game"


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
        Pokemon = self.icon_maker.UI_Maker(
            "Pokemon_HeartGold_Icon", "Pokemon", "HeartGold"
        )
        Pokemon["goto"] = "skill_menu"
        self.icons.append(Pokemon)

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


if __name__ == "__main__":
    window = windows(width, height, title)
    window.setup()
    arcade.run()
