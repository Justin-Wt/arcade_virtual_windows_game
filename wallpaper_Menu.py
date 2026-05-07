#Made in 04 May-Now
#Time: 5hrs
import arcade
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class WallpaperWindow:
    def __init__(self, x, y, w, h, title="Window"):
        self.rect = arcade.XYWH(x=x, y=y, width=w, height=h)
        self.title = title
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self):
        # window body
        arcade.draw_rect_filled(self.rect, arcade.color.DARK_GRAY)

        # title bar (top part)
        title_bar = arcade.Rect(
            self.rect.center_x,
            self.rect.top - 15,
            self.rect.width,
            30
        )
        arcade.draw_rect_filled(title_bar, arcade.color.GRAY)

        arcade.draw_text(
            self.title,
            self.rect.left + 10,
            self.rect.top - 25,
            arcade.color.WHITE,
            14
        )

    def on_mouse_press(self, x, y):
        # check if click is on title bar
        if self.rect.collide_with_point((x, y)):
            self.dragging = True
            self.offset_x = self.rect.center_x - x
            self.offset_y = self.rect.center_y - y

    def on_mouse_release(self):
        self.dragging = False

    def on_mouse_drag(self, x, y):
        if self.dragging:
            self.rect = arcade.Rect(
                x + self.offset_x,
                y + self.offset_y,
                self.rect.width,
                self.rect.height
            )