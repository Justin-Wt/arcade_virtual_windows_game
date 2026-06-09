from ursina import *
import json
import xml.etree.ElementTree as ET
from arkmania_level_engine import Game, Data_Manager


class Episode:
    def __init__(self, path):
        super().__init__()
        self.count = 1
        self.texts = []
        self.path = path
        self.bg = None
        self.selected_id = None
        self.items = None
        self.game = None
        self.unlocks = []
        self.temp_unlocks = []
        self.unlocking = None
        self.bg = []
        self.bgs = []
        self.images = []
        self.lines = []
        self.main_level_buttons = []
        self.sub_level_buttons = []
        self.condition = []
        self.items_tileset = {}
        self.selected_name = None
        self.level_data = {}
        self.bg_tileset = {}
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
        self.items_tileset = self.load_tileset("assets/tile/episodes_item_tilesets.tsx")
        self.bg_tileset = self.load_tileset("assets/tile/episodes_bg_tileset.tsx")
        self.drawing_bg()
        self.creating_ui()

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
        for button in self.main_level_buttons:
            destroy(button)
        for button in self.sub_level_buttons:
            destroy(button)
        for line in self.lines:
            destroy(line)
        self.lines.clear()
        self.main_level_buttons.clear()
        self.sub_level_buttons.clear()
        for item in self.items:
            gid = item["gid"] - 3
            flip_h = bool(gid & 0x80000000)
            flip_v = bool(gid & 0x40000000)
            flip_d = bool(gid & 0x20000000)

            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (item["x"] + item["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (item["y"] - item["height"] / 2) / 1080
            item_image = self.items_tileset.get(tile_id)
            if item["properties"].get("id"):
                if item["properties"]["id"] <= self.count:
                    item["visible"] = True
                else:
                    item["visible"] = False
            else:
                item["visible"] = False
            if item.get("name") in self.unlocks:
                item["visible"] = True
            if item.get("name") in self.temp_unlocks:
                item["visible"] = True
            if item["properties"].get("go_to") in self.unlocks:
                item["visible"] = True
            if item["properties"].get("go_to") in self.temp_unlocks:
                item["visible"] = True
            if not item.get("visible", True):
                continue
            if item["properties"]["type"] == "main":
                button_items = item
                button = Button(
                    item.get("name"),
                    model="quad",
                    parent=camera.ui,
                    texture=item_image,
                    position=(ui_x, ui_y, -0.1),
                    scale=(
                        item["width"] / 1920 * aspect,
                        item["height"] / 1080,
                    ),
                )
                button._on_click = lambda button_item=button_items: self.get_id(
                    button_item
                )
                self.main_level_buttons.append(button)
            elif item["properties"]["type"] == "sub":
                print(item["properties"])
                button_items = item
                unlocks = item["properties"].get("unlocks", None)
                button = Button(
                    item.get("name"),
                    model="quad",
                    parent=camera.ui,
                    texture=item_image,
                    position=(ui_x, ui_y, -0.1),
                    scale=(
                        item["width"] / 1920 * aspect,
                        item["height"] / 1080,
                    ),
                )
                button._on_click = (
                    lambda button_item=button_items, unlocks=unlocks: self.get_sub_id(
                        button_item, unlocks
                    )
                )
                self.sub_level_buttons.append(button)
            else:
                line = Entity(
                    model="quad",
                    parent=camera.ui,
                    texture=item_image,
                    position=(ui_x, ui_y, -0.1),
                    scale=(
                        item["width"] / 1920 * aspect,
                        item["height"] / 1080,
                    ),
                )
                line._double_sided = True
                if flip_h:
                    line.texture_scale = (-1, 1)
                if flip_v:
                    line.texture_scale = (1, -1)
                self.lines.append(line)

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

    def get_sub_id(self, button, unlocks):
        self.selected_id = button["properties"].get("sub_id")
        self.selected_name = button.get("name")
        if unlocks is not None:
            self.unlocking = unlocks
            if unlocks not in self.unlocks:
                if unlocks not in self.temp_unlocks:
                    self.temp_unlocks.append(unlocks)
        self.hide_episode_ui()
        self.game = Game("arkmania.JSON", self.selected_name, self, sub=True)

    def create_winning_condition(self, level):
        data_manager = Data_Manager("arkmania.JSON")
        conditions = data_manager.open_file("Levels", f"Level {level}", "conditions")
        self.condition = conditions.copy()

    def get_id(self, button):
        self.selected_id = button["properties"].get("sub_id")
        self.selected_name = button.get("name")
        self.create_winning_condition(self.selected_name)
        self.hide_episode_ui()
        self.game = Game(
            "arkmania.JSON", self.selected_name, self, False, self.condition
        )

    def return_to_episode(
        self, win=False, sub=False, level=None, first_clear=False, star=0, rewards=[]
    ):
        if win:
            if first_clear:
                if sub:
                    if self.unlocking not in self.unlocks:
                        self.unlocks.append(self.unlocking)
                    if self.unlocking in self.temp_unlocks:
                        self.temp_unlocks.remove(self.unlocking)
                else:
                    self.count += 1
                # self.give_main_reward()
                self.level_data[level] = self.level_data.get(level, {})
                self.level_data[level]["cleared"] = True
                if star == 3:
                    # self.give_special_reward()
                    self.level_data[level]["3 star"] = True
            # else:
            #   self.give_basic_reward()
        else:
            if sub and self.unlocking in self.temp_unlocks:
                self.temp_unlocks.remove(self.unlocking)
        self.creating_ui()
        self.show_episode_ui()

    def hide_episode_ui(self):
        for button in self.main_level_buttons:
            button.enabled = False
            button.visible = False

        for button in self.sub_level_buttons:
            button.enabled = False
            button.visible = False

        for bg in self.bgs:
            bg.enabled = False
            bg.visible = False

        for line in self.lines:
            line.enabled = False
            line.visible = False

        for image in self.images:
            image.visible = False

    def show_episode_ui(self):
        for button in self.main_level_buttons:
            button.enabled = True
            button.visible = True

        for button in self.sub_level_buttons:
            button.enabled = True
            button.visible = True

        for bg in self.bgs:
            bg.enabled = True
            bg.visible = True

        for line in self.lines:
            line.enabled = True
            line.visible = True

        for image in self.images:
            image.visible = True
