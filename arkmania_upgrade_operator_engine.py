from ursina import *
from character_bank import sort_data, add_character, upgrade_character


class Operator:
    def __init__(self):
        self.operator_stuff = sort_data()
        self.buttons = []
        self.sort_button = []
        self.rarity_condition = []
        self.type_condition = []
        self.order_condition = "id"
        self.direction_condition = "ASC"
        self.background = None
        self.button_spacing_x = 0.273
        self.button_spacing_y = 0.4
        self.button_start_positions = (-0.7279620853080568, 0.225)
        self.create_ui()

    def create_ui(self):
        self.create_bg()
        self.create_sort_button()
        self.create_button()

    def create_bg(self):
        self.back_ground = Entity(
            model="quad",
            parent=camera.ui,
            texture="assets/picture/backgrounds/background_1.png",
            scale=(2, 1),
        )

    def create_sort_button(self):
        button = Button(
            model="quad",
            parent=camera.ui,
            position=(0.8, 0.4),
            scale=(0.2, 0.1),
            color=color.rgba(0.6, 0.6, 0.6, 0.6),
            z=-0.1,
        )
        button.on_click = lambda: self.sorting("rarity", "5")
        text = Text(
            "5 Star",
            parent=camera.ui,
            position=(0.8, 0.4),
            origin=(0, 0),
            color=color.black,
            z=-1,
        )

    def sorting(self, types, value):
        if types == "rarity":
            self.rarity_condition.append(value)
        elif types == "type":
            self.type_condition.append(value)
        elif types == "order":
            self.order_condition = value
        else:
            self.direction_condition = value
        sort_data(
            self.order_condition,
            self.direction_condition,
            self.rarity_condition,
            self.type_condition,
        )

    def create_button(self):
        for i, items in enumerate(self.operator_stuff):
            character_name = items.get("name")
            character_level = items.get("level")
            x, y = self.button_start_positions
            button_bg = Button(
                parent=camera.ui,
                model="quad",
                position=(
                    x + (i // 2 * self.button_spacing_x),
                    y - (i % 2 * self.button_spacing_y),
                    -0.1,
                ),
                color=color.rgba(0.6, 0.6, 0.6, 0.6),
                scale=(0.2, 0.38),
            )
            character_image = Entity(
                model="quad",
                parent=camera.ui,
                texture=(
                    f"assets/picture/characters/{character_name}_tier_1.png"
                    if items.get("awaken") == False
                    else f"assets/picture/characters/{character_name}_tier_2.png"
                ),
                position=(
                    x + (i // 2 * self.button_spacing_x),
                    y - (i % 2 * self.button_spacing_y),
                    -0.1,
                ),
                color=color.rgba(1, 1, 1, 1),
                scale=(0.2, 0.38),
            )
            level = Text(
                text=f"LV.\n{character_level}",
                parent=camera.ui,
                position=(
                    x + (i // 2 * self.button_spacing_x) + 0.07,
                    y - (i % 2 * self.button_spacing_y) - 0.15,
                ),
                origin=(0, 0),
                color=color.black,
                z=-1,
            )


if __name__ == "__main__":
    app = Ursina(
        title="Arkmania", icon="assets/icons/Arkmania_Icon.ico", development_mode=False
    )
    window.borderless = False
    window.fullscreen = False
    window.size = (1280, 720)
    Operator()
    EditorCamera()
    app.run()
