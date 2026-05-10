# Made in May 07
import arcade
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class icon_maker:
    def __init__(self, width, height):
        self.icon = 0
        self.width = width
        self.height = height
        self.bg = None

    def create_icon(self, image, texts1, texts2, direction, width, height):
        if direction == "Vertical":
            row = (self.icon % 8) * 100 + 50
            column = (self.icon // 8) * 100 + width // 2 + 20
        else:
            column = (self.icon % 4) * width * 1.2 + width // 2 + 20
            row = (self.icon // 4) * 100 + 50
        x = column
        y = self.height - row - height // 4
        text1_y = y - height / 2 - 12.5
        text2_y = y - height / 2 - 22.5
        text1_x = column - (len(texts1) * 4)
        text2_x = column - (len(texts2) * 4)
        rect = x, y, width, height
        try:
            texture = arcade.load_texture(
                os.path.join(BASE_DIR, "assets", "UI's", f"{image}.png")
            )
        except Exception:
            texture = arcade.load_texture(
                os.path.join(
                    BASE_DIR, "assets", "UI's", "Backgrounds", image, f"{image}0.png"
                )
            )
        text1 = arcade.Text(
            texts1,
            text1_x,
            text1_y,
            arcade.color.WHITE,
            font_size=14,
        )
        text2 = arcade.Text(
            texts2,
            text2_x,
            text2_y,
            arcade.color.WHITE,
            font_size=14,
        )
        self.icon += 1
        if direction == "Vertical":
            return {
                "rect": rect,
                "texture": texture,
                "text": (text1, text2),
            }
        else:
            return {
                "rect": rect,
                "texture": texture,
                "text": (texts1, texts2, text1_x, text1_y, text2_x, text2_y),
            }

    def UI_Maker(
        self, image, text1, text2="", direction="Vertical", width=50, height=50
    ):
        data = self.create_icon(image, text1, text2, direction, width, height)
        return {
            "image": image,
            "clicked": False,
            "hover": False,
            "enter": False,
            **data,
        }
