from ursina import *
import json
import os
import xml.etree.ElementTree as ET
from arkmania_character_showcase_engine import Operator_Showcase
from character_bank import sort_data, upgrade_character, add_character


class Operator:
    def __init__(self, main_menu, upgrade_path="assets/tile/upgrade.tmj"):
        self.main_menu = main_menu
        self.ui_ungrouped = []
        self.path = upgrade_path
        self.character_data = None
        self.uis = []
        self.button_tileset = {}
        self.bg_tileset = {}
        self.bg = []
        self.data = []
        self.buttons = []
        self.leave_button = None
        self.bgs = []
        Operator_Showcase(self)

    def opening_path(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        layers = data["layers"]
        self.bg = next(layer["objects"] for layer in layers if layer["name"] == "bg")
        self.ui_ungrouped = next(
            layer["objects"] for layer in layers if layer["name"] == "ui"
        )
        self.getting_object(self.ui_ungrouped)

    def getting_object(self, objects):
        for obj in objects:
            obj["properties"] = {
                p["name"]: p["value"] for p in obj.get("properties", [])
            }
        self.button_tileset = self.load_tileset("assets/tile/item_tilesets.tsx")
        self.bg_tileset = self.load_tileset("assets/tile/bg_tilesets.tsx")
        for obj in objects:
            self.uis.append([obj, obj["properties"]["type"]])
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
        for item in self.uis:
            ui, ui_type = item
            gid = ui["gid"] - 5
            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (ui["x"] + ui["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (ui["y"] - ui["height"] / 2) / 1080
            item_image = (
                f"assets/picture/ui's/{ui_type}.png"
                if ui_type not in ("operator", "logo")
                else (
                    f"assets/picture/characters/{self.character_data['name']}_tier_1.png"
                    if ui_type == "operator" and self.character_data["awaken"] == 0
                    else (
                        f"assets/picture/characters/{self.character_data['name']}_tier_2.png"
                        if ui_type == "operator"
                        else (
                            f"assets/types/{self.character_data['type']}.png"
                            if self.character_data["awaken"] == 0
                            else f"assets/types/{self.character_data['type']} Awaken.png"
                        )
                    )
                )
            )
            ui["visible"] = True
            if item_image != self.button_tileset.get(tile_id):
                bg = Entity(
                    model="quad",
                    parent=camera.ui,
                    position=(ui_x, ui_y, -0.05),
                    color=color.rgba(0.2, 0.2, 0.2, 0.6),
                    scale=(
                        ui["width"] / 1920 * aspect,
                        ui["height"] / 1080,
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
                    ui["width"] / 1920 * aspect,
                    ui["height"] / 1080,
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
        if self.leave_button:
            destroy(self.leave_button)
        self.uis.clear()
        self.ui_ungrouped.clear()

    def leaving(self):
        self.destroying()
        self.main_menu.return_to_main_menu()

    def pick(self, i):
        self.destroying()
        self.picked_slot = i
        Operator_Showcase(self)

    def character_button_clicked(self, items="none"):
        if items != "none":
            self.character_data = items
            self.opening_path(self.path)
        else:
            self.destroying()
            self.main_menu.return_to_main_menu()


if __name__ == "__main__":
    app = Ursina(
        title="Arkmania", icon="assets/icons/Arkmania_Icon.ico", development_mode=False
    )
    window.borderless = False
    window.fullscreen = False
    window.size = (1280, 720)
    Operator("i dunno")
    EditorCamera()
    app.run()
