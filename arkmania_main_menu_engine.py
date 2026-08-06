# Time_In: {
#   Blender: "18 Hrs"
#   Python : "50 Hrs"
#   Tiled  : "3 hrs:
# }

from ursina import *
import json
import xml.etree.ElementTree as ET
from arkmania_episode_pick_engine import Episode
from arkmania_upgrade_operator_engine import Operator
from arkmania_squad_engine import Squad

# from arkmania_add_stamina_engine import Stamina
# from arkmania_event_billboard_engine import Bilboard
# from arkmania_store_engine import Store
# from arkmania_summon_engine import Recruit, HeadHunt
# from arkmania_friend_engine import Friends
# from arkmania_archieve_engine import Archieves
# from arkmania_mission_engine import Mission
# from arkmania_base_engine import Base
# from arkmania_depot_engine import Depot


class main_menu:
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.items = None
        self.bg = []
        self.bgs = []
        self.buttons = []
        self.items_tileset = {}
        self.engines = {
            "Episode": Episode,
            "Squads": Squad,
            "Operator": Operator,
            # "Store" : Store,
            # "Recruit" : Recruit,
            # "Billboard" : Billboard,
            # "Friends" : Friends,
            # "Archieves" : Archieves,
            # "HeadHunt" : Headhunt,
            # "Mission" : Mission,
            # "Base" : Base,
            # "Depot" : Depot,
            # "Stamina" : Stamina
        }
        self.bg_tileset = {}
        self.opening_path(self.path)
        self.input_entity = Entity()
        self.update_entity = Entity()
        self.input_entity.input = self.input
        self.update_entity.update = self.update

    def opening_path(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        layers = data["layers"]
        self.bg = next(layer["objects"] for layer in layers if layer["name"] == "bg")
        self.items = next(
            layer["objects"] for layer in layers if layer["name"] == "items"
        )
        self.getting_object(self.items)

    def getting_object(self, objects):
        for obj in objects:
            obj["properties"] = {
                p["name"]: p["value"] for p in obj.get("properties", [])
            }
        self.items_tileset = self.load_tileset("assets/tile/item_tilesets.tsx")
        self.bg_tileset = self.load_tileset("assets/tile/bg_tilesets.tsx")
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
        for button in self.buttons:
            destroy(button)
        self.buttons.clear()
        for item in self.items:
            gid = item["gid"] - 4

            gid &= ~(0x80000000 | 0x40000000 | 0x20000000)
            tile_id = gid
            aspect = window.aspect_ratio
            ui_x = (item["x"] + item["width"] / 2) / 1920 * aspect - aspect / 2
            ui_y = 0.5 - (item["y"] - item["height"] / 2) / 1080
            item_image = self.items_tileset.get(tile_id)
            item["visible"] = True
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

    def run(self, engine_name):
        self.destroy_ui()
        engine = self.engines.get(engine_name)
        if engine:
            engine(self)

    def destroy_ui(self):
        for bg in self.bgs:
            destroy(bg)
        for button in self.buttons:
            destroy(button)
        self.bgs.clear()
        self.buttons.clear()

    def return_to_main_menu(self):
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

    def input(self, key):
        pass

    def update(self):
        pass
