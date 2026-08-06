from ursina import *
import json
import os
import xml.etree.ElementTree as ET
from arkmania_character_showcase_engine import Operator_Showcase
from character_bank import sort_data

# improvement: make operators, use cvs, reading json the covert stuff


class Squad:
    def __init__(self, main_menu, squad_path="assets/tile/squads.tmj"):
        self.picked_line_up = "Arkmania_Squad.JSON"
        self.button_ungrouped = []
        self.path = squad_path
        self.main_menu = main_menu
        self.character_data = sort_data()
        self.button = []
        self.leave_button = None
        self.squad_button = []
        self.picked_slot = None
        self.button_tileset = {}
        self.bg_tileset = {}
        self.bg = []
        self.data = []
        self.buttons = []
        self.picked_squad_slot = "slot 1"
        self.bgs = []
        self.line_up = self.load_buttons()
        self.opening_path(self.path)

    def load_buttons(self):
        path = self.picked_line_up
        if not os.path.exists(path):
            # create file with empty JSON structurez
            with open(path, "w") as f:
                json.dump(
                    {
                        "slot 1": [
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                        "slot 2": [
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                        "slot 3": [
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                        "slot 4": [
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                            "none",
                        ],
                    },
                    f,
                )
        with open(path, "r") as f:
            self.data = json.load(f)

    def opening_path(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        layers = data["layers"]
        self.bg = next(layer["objects"] for layer in layers if layer["name"] == "bg")
        self.button_ungrouped = next(
            layer["objects"] for layer in layers if layer["name"] == "buttons"
        )
        self.getting_object(self.button_ungrouped)

    def getting_object(self, objects):
        for obj in objects:
            obj["properties"] = {
                p["name"]: p["value"] for p in obj.get("properties", [])
            }
        self.button_tileset = self.load_tileset("assets/tile/item_tilesets.tsx")
        self.bg_tileset = self.load_tileset("assets/tile/bg_tilesets.tsx")
        for obj in objects:
            if obj["properties"]["type"] == "op_button":
                self.button.append(obj)
            else:
                self.squad_button.append(obj)
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
        for i, item in enumerate(self.button):
            gid = item["gid"] - 5
            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (item["x"] + item["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (item["y"] - item["height"] / 2) / 1080
            item_image = next(
                (
                    f"assets/picture/characters/{char.get('name')}_{'tier_2' if char.get('awaken') else 'tier_1'}.png"
                    for char in self.character_data
                    if char.get("name") == self.data.get(self.picked_squad_slot)[i]
                ),
                self.button_tileset.get(tile_id),
            )
            char_level = next(
                (
                    f"{char.get("level")}"
                    for char in self.character_data
                    if char.get("name") == self.data.get(self.picked_squad_slot)[i]
                ),
                "none",
            )
            item["visible"] = True
            if item_image != self.button_tileset.get(tile_id):
                bg = Entity(
                    model="quad",
                    parent=camera.ui,
                    position=(ui_x, ui_y, -0.05),
                    color=color.rgba(0.2, 0.2, 0.2, 0.6),
                    scale=(
                        item["width"] / 1920 * aspect,
                        item["height"] / 1080,
                    ),
                )
                self.buttons.append(bg)
            button = Button(
                model="quad",
                parent=camera.ui,
                texture=item_image,
                position=(ui_x, ui_y, -0.1),
                color=(
                    color.rgba(0.2, 0.2, 0.2, 0.6)
                    if item_image == self.button_tileset.get(tile_id)
                    else color.white
                ),
                scale=(
                    item["width"] / 1920 * aspect,
                    item["height"] / 1080,
                ),
            )
            button.on_click = lambda engine=i: self.pick(engine)
            self.buttons.append(button)
            level = Text(
                text=f"LV.\n{char_level}" if char_level != "none" else "",
                parent=camera.ui,
                position=(
                    ui_x + 0.07,
                    ui_y - 0.15,
                ),
                origin=(0, 0),
                color=color.black,
                z=-1,
            )
            self.buttons.append(level)
        for item in self.squad_button:
            gid = item["gid"] - 5
            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (item["x"] + item["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (item["y"] - item["height"] / 2) / 1080
            item_image = self.button_tileset.get(tile_id)
            item["visible"] = True
            button = Button(
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
            self.buttons.append(button)
        self.leave_button = Button(
            text="<-",
            parent=camera.ui,
            model="quad",
            position=(-0.82, 0.475),
            scale=(0.15, 0.05),
            color=color.red,
        )
        self.leave_button.on_click = lambda: self.leaving()

    def destroying(self):
        for button in self.buttons:
            destroy(button)
        for bg in self.bgs:
            destroy(bg)
        self.button.clear()
        self.button_ungrouped.clear()
        destroy(self.leave_button)

    def leaving(self):
        self.destroying()
        self.main_menu.return_to_main_menu()

    def pick(self, i):
        self.destroying()
        self.picked_slot = i
        Operator_Showcase(self)

    def character_button_clicked(self, items="none"):
        if items != "none":
            for i, slots in enumerate(self.data.get(self.picked_squad_slot)):
                if slots == items.get("name"):
                    self.data.get(self.picked_squad_slot)[i] = "none"
            self.data.get(self.picked_squad_slot)[self.picked_slot] = items.get("name")
            self.save()
        self.opening_path(self.path)

    def save(self):
        with open(self.picked_line_up, "w") as f:
            json.dump(self.data, f, indent=4)


if __name__ == "__main__":
    app = Ursina(
        title="Arkmania", icon="assets/icons/Arkmania_Icon.ico", development_mode=False
    )
    window.borderless = False
    window.fullscreen = False
    window.size = (1280, 720)
    Squad("i dunno")
    EditorCamera()
    app.run()
