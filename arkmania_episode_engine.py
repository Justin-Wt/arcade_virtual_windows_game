from ursina import *
import json
from direct.actor.Actor import Actor
import xml.etree.ElementTree as ET

tree = ET.parse("assets/tile/episodes_item_tilesets.tsx")
root = tree.getroot()
image = root.find("image")
png_path = image.attrib["source"]
print(png_path)
app = Ursina()


class Episode:
    def __init__(self, path):
        super().__init__()
        self.count = 1
        self.texts = []
        self.path = path
        self.bg = None
        self.items = None
        self.bg = []
        self.images = []
        self.buttons = []
        self.opening_path(self.path)

    def opening_path(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        layers = data["layers"]
        self.bg = next(
            layer["objects"] for layer in layers if layer["name"] == "episode_bg"
        )
        self.items = next(
            layer["objects"] for layer in layers if layer["name"] == "items"
        )
        self.getting_object(self.items)

    def getting_object(self, objects):
        for obj in objects:
            obj["properties"] = {
                p["name"]: p["value"] for p in obj.get("properties", [])
            }
        self.creating_ui()

    def creating_ui(self):
        for item in self.items:
            if item["properties"]["id"] <= self.count:
                item["visible"] = True
                print(item["properties"])
                if (
                    item["properties"]["type"] == "main"
                    or item["properties"]["type"] == "sub"
                ):
                    print("button")
            else:
                item["visible"] = False

    # def on_draw(self):
    #     self.clear()
    #     self.bg.draw()
    #     self.items.draw()
    #     if self.texts:
    #         for text in self.texts:
    #             text.draw()

    # def on_mouse_press(self, x, y, button, modifiers):
    #     self.count += 1
    #     self.refresh()

    # def refresh(self):
    #     self.texts.clear()
    #     for item in self.items:
    #         if item.properties["id"] <= self.count:
    #             item.visible = True
    #             print(item.properties)
    #             if (
    #                 item.properties["type"] == "main"
    #                 or item.properties["type"] == "sub"
    #             ):
    #                 text = arcade.Text(
    #                     item.properties["name"],
    #                     item.center_x - len(item.properties["name"]) * 7,
    #                     item.center_y - font // 2,
    #                     arcade.color.WHITE,
    #                     font,
    #                 )
    #                 self.texts.append(text)
    #         else:
    #             item.visible = False


# window = arcade.Window(1920, 1080, "Testing")
# window.game_view = Episode("assets/tile/episode_1.tmj")
# window.show_view(window.game_view)
# arcade.run()

game = Episode("assets/tile/episode_1.tmj")
EditorCamera()
app.run()
