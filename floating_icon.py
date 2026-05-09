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
        rect = x, y, width, height
        try:
            texture = arcade.load_texture(
                os.path.join(BASE_DIR, "assets", "UI's", f"{image}.png")
            )
        except Exception:
            texture = arcade.load_texture(
                os.path.join(BASE_DIR, "assets", "UI's", image, f"{image}0.png")
            )
        text1 = arcade.Text(
            texts1,
            column - (len(texts1) * 4),
            y - height / 2 - 12.5,
            arcade.color.WHITE,
            font_size=14,
        )
        text2 = arcade.Text(
            texts2,
            column - (len(texts2) * 4),
            y - height / 2 - 22.5,
            arcade.color.WHITE,
            font_size=14,
        )
        self.icon += 1
        return {"rect": rect, "texture": texture, "text": (text1, text2)}

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
