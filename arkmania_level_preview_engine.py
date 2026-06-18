from ursina import *
from arkmania_level_engine import Game
from datamanager import Data_Manager
import textwrap


class Level_Preview:
    def __init__(
        self,
        filename="arkmania.JSON",
        level="1-1",
        episode_name="Episode 1",
        episode="stuff",
        sub=False,
        condition=[],
    ):
        self.current_episode = episode_name
        self.episode = episode
        self.buttons = self.create_buttons()
        self.level = level
        self.sub = sub
        self.condition = condition
        self.level_enemy_name = []
        self.backgrounds = []
        self.texts = []
        self.loot = []
        self.desc_panel = []
        self.desc_text = []
        for e in scene.entities:
            if isinstance(e, EditorCamera):
                self.camera = e
        self.loot_button = []
        self.loot_frame = []
        self.enemy_content = None
        self.loot_content = None
        self.enemy_panel_scroll_y = 0
        self.loot_panel_scroll_x = 0
        self.enemy_panel = None
        self.loot_panel = None
        self.filename = filename
        self.data_manager = Data_Manager(self.filename)
        self.grid, self.tiles = self.tile_maker(self.level)
        self.show_info()

        self.input_entity = Entity()
        self.update_entity = Entity()
        self.input_entity.input = self.input
        self.update_entity.update = self.update

    def create_buttons(self):
        leave_button = Button(
            text="X",
            parent=camera.ui,
            model="quad",
            position=(-0.82, 0.475),
            scale=(0.15, 0.05),
            color=color.red,
        )
        leave_button.on_click = lambda: self.leaving()
        next_button = Button(
            text="->",
            parent=camera.ui,
            model="quad",
            position=(0.75, -0.45),
            scale=(0.3, 0.1),
            color=color.white,
            text_color=color.gray,
            text_size=2,
        )
        next_button.on_click = lambda: self.enter_level()
        return [leave_button, next_button]

    def enter_level(self):
        self.hide_ui()
        Game(
            filename=self.filename,
            level=self.level,
            episode=self.episode,
            sub=self.sub,
            condition=self.condition,
            current_episode=self.current_episode,
        )

    def leaving(self):
        self.hide_ui()
        self.episode.return_to_episode()

    def hide_ui(self):
        destroy(self.enemy_panel)
        destroy(self.loot_panel)

        for bg in self.backgrounds:
            destroy(bg)

        for button in self.buttons:
            destroy(button)

        for tile in self.tiles:
            destroy(tile)

        if self.texts:
            for text in self.texts:
                destroy(text)

        destroy(self.input_entity)
        destroy(self.update_entity)
        self.enemy_content = None
        self.enemy_panel = None
        self.loot_content = None
        self.loot_panel = None
        self.grid.clear()
        self.tiles.clear()
        self.buttons.clear()
        self.level_enemy_name.clear()
        self.loot_button.clear()
        self.loot_frame.clear()
        self.loot.clear()
        self.backgrounds.clear()
        self.texts.clear()

    def tile_maker(self, level):
        grid = self.data_manager.open_file(
            "Episodes", self.current_episode, f"Level {level}", "grid"
        )
        tiles = []
        for x in range(len(grid)):
            for z in range(len(grid[0])):
                index = grid[z][x]
                height = 1 if index > 0 else -0.2
                tile = Entity(
                    model="cube",
                    scale=(1, (0.1 + height if height > 0 else 0.1), 1),
                    position=(x, height / 2, z),
                    texture="white_cube",
                    index=index,
                    color=(
                        color.rgba(0, 0, 0.8, 0.85)
                        if index == 3
                        else (color.rgba(0.8, 0, 0, 0.85) if index == 2 else color.gray)
                    ),
                    collider="box",
                )
                tiles.append(tile)
                if index > 0:
                    tile = Entity(
                        model="cube",
                        scale=(1, 0.1, 1),
                        position=(x, -0.1, z),
                        texture="white_cube",
                        index=index if index < 2 else 9,
                        color=color.gray,
                        collider="box",
                    )
                    tiles.append(tile)

        return grid, tiles

    def update_cube_color(self):
        for cube in self.tiles:
            if cube.index == 3:
                cube.color = color.rgba(0, 0, 0.8, 0.85)
            elif cube.index == 2:
                cube.color = color.rgba(0.8, 0, 0, 0.85)
            else:
                cube.color = color.gray

    def show_info(self):
        self.show_enemy_info()
        self.show_level_info()
        self.show_loot_info()

    def show_loot_info(self):
        datas = self.data_manager.open_file(
            "Episodes", self.current_episode, f"Level {self.level}", "rewards"
        )
        for loot_types, lootable in datas.items():
            for loots in lootable:
                loot = loots.get("item")
                loot_type = loot_types
                self.loot.append([loot_type, loot])
        self.loot_panel = Entity(
            parent=camera.ui,
            name="panel",
            model="quad",
            color=color.rgba(0, 0, 0, 0.45),
            scale=(2, 0.15),
            position=(0, -0.3),
            collider=None,
        )
        self.loot_content = Entity(parent=self.loot_panel, scale=(0.15, 2, 1))
        for i, (loot_type, loot) in enumerate(self.loot):
            button = Button(
                name="loot",
                color=color.white,
                parent=self.loot_content,
                origin=(0, 0),
                scale=(0.4, 0.4),
                texture=f"assets/picture/items/{loot}.png",
                position=(-0.3 + (i * 0.625), 0),
            )
            frame = Entity(
                name="frame",
                model="quad",
                parent=self.loot_content,
                color=color.white,
                origin=(0, 0),
                scale=(0.6, 0.6),
                texture=f"assets/picture/items/{loot_type}_frame.png",
                position=(-0.3 + (i * 0.625), 0, -0.01),
            )
            # button.on_click = lambda loot_name=loot: self.show_desc(loot_name)
            self.loot_frame.append(frame)
            self.loot_button.append(button)

    # def show_desc(self):
    #     for panel in self.desc_panel:
    #         destroy(panel)
    #     for desc in self.desc_text:
    #         destroy(desc)

    #     item_desc = self.data_manager.open_file(
    #         "Episodes",
    #         self.current_episode,
    #         f"Level {self.level}, rewards",
    #     )
    #     wrapped_lines = textwrap.wrap(item_desc, width=25)

    def show_level_info(self):
        background = Entity(
            parent=camera.ui,
            model="quad",
            position=(0, 0.45),
            color=color.rgba(0, 0, 0, 0.4),
            scale=(0.5, 0.1),
            z=1,
        )
        self.backgrounds.append(background)
        txt = Text(
            f"Level {self.level}",
            name="title",
            parent=camera.ui,
            origin=(0, 0),
            scale=2,
            position=(0, 0.45),
            color=color.white,
            z=-1,
        )
        self.texts.append(txt)

    def show_enemy_info(self):
        datas = self.data_manager.open_file(
            "Episodes",
            self.current_episode,
            f"Level {self.level}",
            "waves",
        )
        for items in datas:
            for item in items["spawns"]:
                enemy_type = item["enemy_type"]
                if enemy_type not in self.level_enemy_name:
                    self.level_enemy_name.append(enemy_type)
        txt = Text(
            "Enemy Preview",
            name="title",
            origin=(0, 0),
            scale=2,
            position=(-0.65, 0.36),
            color=color.white,
        )
        self.texts.append(txt)
        self.enemy_panel = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgba(0, 0, 0, 0.4),
            scale=(0.5, 0.6),
            position=(-0.625, 0.1),
            collider="box",
        )
        self.enemy_content = Entity(parent=self.enemy_panel)
        for i, enemy_name in enumerate(self.level_enemy_name):
            enemy_desc = self.data_manager.open_file("Enemies", enemy_name, "info")
            wrapped_lines = textwrap.wrap(enemy_desc, width=25)
            txt = Text(
                enemy_name,
                name="enemy_name_text",
                parent=self.enemy_content,
                origin=(0, 0),
                scale=3,
                position=(-0.4, 0.3 - (i * 0.375)),
                color=color.lime,
            )
            self.texts.append(txt)
            for line_num, line in enumerate(wrapped_lines):
                txt = Text(
                    line,
                    name="enemy_desc_text",
                    parent=self.enemy_content,
                    origin=(-0.5, 0.5),
                    scale=1.875,
                    position=(-0.44, 0.265 - (i * 0.375) - (line_num * 0.0375)),
                    color=color.white,
                )
                self.texts.append(txt)

    def mouse_hover_panel(self):
        return -1 <= mouse.x <= 1 and -0.375 <= mouse.y <= -0.225

    def input(self, key):
        if self.mouse_hover_panel() or mouse.hovered_entity == self.enemy_panel:
            if key == "scroll down" or key == "scroll up":
                self.camera.rotation_speed = 0
                self.camera.move_speed = 0
                self.camera.zoom_speed = 0
            else:
                self.camera.rotation_speed = 200
                self.camera.move_speed = 10
                self.camera.zoom_speed = 1.25
        else:
            self.camera.rotation_speed = 200
            self.camera.move_speed = 10
            self.camera.zoom_speed = 1.25
        if self.mouse_hover_panel():
            if key == "scroll up":
                self.loot_panel_scroll_x += 0.02
            elif key == "scroll down":
                self.loot_panel_scroll_x -= 0.02
            self.loot_panel_scroll_x = min(self.loot_panel_scroll_x, 0.2)
            self.loot_content.x = self.loot_panel_scroll_x
        if mouse.hovered_entity == self.enemy_panel:
            if key == "scroll up":
                self.enemy_panel_scroll_y += 0.02
            elif key == "scroll down":
                self.enemy_panel_scroll_y -= 0.02
            self.enemy_panel_scroll_y = clamp(self.enemy_panel_scroll_y, 0, 1.5)
            self.enemy_content.y = self.enemy_panel_scroll_y

    def update(self):
        self.update_cube_color()
        for button in self.loot_button:
            left_distance = button.world_x - (-12.5)
            right_distance = 18.25 - button.world_x
            distance = min(left_distance, right_distance)
            alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0
            button.alpha = alpha
        for frame in self.loot_frame:
            left_distance = frame.world_x - (-12.5)
            right_distance = 18.25 - frame.world_x
            distance = min(left_distance, right_distance)
            alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0
            frame.alpha = alpha
        for text in self.texts:
            if text.name != "title":
                up_distance = 6.7 - text.world_y
                down_distance = text.world_y + 3.3
                distance = min(up_distance, down_distance)
                text.alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0


if __name__ == "__main__":
    app = Ursina()
    EditorCamera()
    app.run()
