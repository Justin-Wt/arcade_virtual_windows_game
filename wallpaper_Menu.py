# Made in 07 May-09 May
# 1 hrs
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
        self.scroll_y = 0
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
        Cyberpunk_Room_Wallpaper = self.icon_maker.UI_Maker(
            "Cyberpunk_Room", "Cyberpunk", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Cyberpunk_Room_Wallpaper["frames"] = 195
        self.icons.append(Cyberpunk_Room_Wallpaper)
        Goku_Wallpaper = self.icon_maker.UI_Maker(
            "Goku", "Goku", "(Normal Wallpaper)", "Horizontal", 150, 75
        )
        Goku_Wallpaper["frames"] = 1
        self.icons.append(Goku_Wallpaper)
        Japan_Wallpaper = self.icon_maker.UI_Maker(
            "Japan", "japan", "(Normal Wallpaper)", "Horizontal", 150, 75
        )
        Japan_Wallpaper["frames"] = 1
        self.icons.append(Japan_Wallpaper)
        Kaltsit_Wallpaper = self.icon_maker.UI_Maker(
            "Kaltsit", "kaltsit", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Kaltsit_Wallpaper["frames"] = 178
        self.icons.append(Kaltsit_Wallpaper)
        Makima_Wallpaper = self.icon_maker.UI_Maker(
            "Makima", "Makima", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Makima_Wallpaper["frames"] = 190
        self.icons.append(Makima_Wallpaper)
        Pragmata_Wallpaper = self.icon_maker.UI_Maker(
            "Pragmata", "Pragmata", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Pragmata_Wallpaper["frames"] = 129
        self.icons.append(Pragmata_Wallpaper)
        Silver_Wolf_Wallpaper = self.icon_maker.UI_Maker(
            "Silver_Wolf", "Silver Wolf", "(L2D Wallpaper)", "Horizontal", 150, 75
        )
        Silver_Wolf_Wallpaper["frames"] = 80
        self.icons.append(Silver_Wolf_Wallpaper)
        Zenitsu_Wallpaper = self.icon_maker.UI_Maker(
            "Zenitsu", "Zenitsu", "(Normal Wallpaper)", "Horizontal", 150, 75
        )
        Zenitsu_Wallpaper["frames"] = 1
        self.icons.append(Zenitsu_Wallpaper)
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
            draw_y = y + self.scroll_y
            if icon["clicked"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, draw_y - 10, w + 27, h + 32), (0, 0, 0, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, draw_y - 10, w + 25, h + 30),
                    (150, 150, 150, 200),
                )
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(x, draw_y, w + 20, h + 20), (0, 0, 139, 0)
                )
            if icon["hover"]:
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, draw_y - 10, w + 27, h + 32), (0, 0, 0, 150)
                )
                arcade.draw_rect_filled(
                    arcade.XYWH(x + 3, draw_y - 10, w + 25, h + 30),
                    (150, 150, 150, 200),
                )
            arcade.draw_texture_rect(icon["texture"], arcade.XYWH(x, draw_y, w, h))
            text1, text2, x1, y1, x2, y2 = icon["text"]
            text_1 = arcade.Text(text1, x1, y1, arcade.color.WHITE, 14)
            text_2 = arcade.Text(text2, x2, y2, arcade.color.WHITE, 14)
            text_1.y = y1 + self.scroll_y
            text_2.y = y2 + self.scroll_y
            text_1.draw()
            text_2.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scroll_y -= scroll_y * 30
        if self.scroll_y <= -30:
            self.scroll_y = 0
        x, y, w, h = self.icons[-1]["rect"]
        print(y + self.scroll_y)

    def on_mouse_motion(self, x, y, dx, dy):
        for icon in self.icons:
            rx, ry, rw, rh = icon["rect"]
            left = rx - rw / 2
            right = rx + rw / 2
            bottom = (ry + self.scroll_y) - rh / 2
            up = (ry + self.scroll_y) + rh / 2
            if (left <= x <= right) and (bottom <= y <= up):
                icon["hover"] = True
            else:
                icon["hover"] = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        for icon in self.icons:
            rx, ry, rw, rh = icon["rect"]
            left = rx - rw / 2
            right = rx + rw / 2
            bottom = (ry + self.scroll_y) - rh / 2
            up = (ry + self.scroll_y) + rh / 2
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
