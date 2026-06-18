from ursina import *
import json
import os
import xml.etree.ElementTree as ET

# LINEUP_FILE = ["Line-UP1.JSON", "Line-UP2.JSON", "Line-UP3.JSON", "Line-UP4.JSON"]
# improvement: make operators, use cvs, reading json the covert stuff


class Squad:
    def __init__(self):
        self.picked_line_up = "Line-UP1.JSON"
        self.button = None
        self.button_tileset = {}
        self.bg_tileset = {}
        self.bg = []
        self.buttons = []
        self.bgs = []
        self.line_up = self.load_buttons()
        self.opening_path("assets/tile/squads.tmj")

    def load_buttons(self):
        path = self.picked_line_up
        if not os.path.exists(path):
            # create file with empty JSON structurez
            with open(path, "w") as f:
                json.dump({}, f)
        with open(path, "r") as f:
            data = json.load(f)

    def opening_path(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        layers = data["layers"]
        self.bg = next(layer["objects"] for layer in layers if layer["name"] == "bg")
        self.button = next(
            layer["objects"] for layer in layers if layer["name"] == "buttons"
        )
        self.getting_object(self.button)

    def getting_object(self, objects):
        for obj in objects:
            obj["properties"] = {
                p["name"]: p["value"] for p in obj.get("properties", [])
            }
        self.button_tileset = self.load_tileset("assets/tile/item_tilesets.tsx")
        self.bg_tileset = self.load_tileset("assets/tile/bg_tilesets.tsx")
        self.drawing_bg()
        self.creating_ui()

    def load_tileset(self, tsx_path):
        tree = ET.parse(tsx_path)
        root = tree.getroot()
        tile_images = {}
        for tile in root.findall("tile"):
            tile_id = int(tile.attrib["id"])
            image = tile.find("image")
            image_path = image.attrib["source"]
            tile_images[tile_id] = image_path
        return tile_images

    def drawing_bg(self):
        for bg in self.bg:
            gid = bg["gid"] - 1
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (bg["x"] + bg["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (bg["y"] - bg["height"] / 2) / 1080
            bg_image = self.bg_tileset.get(tile_id)
            bg["visible"] = True
            back_ground = Entity(
                model="quad",
                parent=camera.ui,
                texture=bg_image,
                position=(ui_x, ui_y),
                scale=(
                    bg["width"] / 1920 * aspect,
                    bg["height"] / 1080,
                ),
            )
            self.bgs.append(back_ground)

    def creating_ui(self):
        for button in self.buttons:
            destroy(button)
        self.buttons.clear()
        for item in self.button:
            gid = item["gid"] - 5
            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (item["x"] + item["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (item["y"] - item["height"] / 2) / 1080
            item_image = self.button_tileset.get(tile_id)
            item["visible"] = True
            print(ui_x)
            print(ui_y)
            print()
            # name:
            # Episode
            # Squads
            # Operator
            # Store
            # Recruit
            # Billboard
            # Friends
            # Archieves
            # HeadHunt
            # Mission
            # Base
            # Depot
            # Stamina
            button = Button(
                item.get("name"),
                model="quad",
                parent=camera.ui,
                texture=item_image,
                position=(ui_x, ui_y, -0.1),
                color=color.rgba(0.2, 0.2, 0.2, 0.6),
                scale=(
                    item["width"] / 1920 * aspect,
                    item["height"] / 1080,
                ),
            )
            button.on_click = lambda engine=item.get("name"): self.run(engine)
            self.buttons.append(button)


if __name__ == "__main__":
    app = Ursina(
        title="Arkmania", icon="assets/icons/Arkmania_Icon.ico", development_mode=False
    )
    window.borderless = False
    window.fullscreen = False
    window.size = (1280, 720)
    Squad()
    EditorCamera()
    app.run()
