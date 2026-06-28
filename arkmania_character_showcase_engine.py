from ursina import *
from character_bank import sort_data, add_character, upgrade_character


class Operator:
    def __init__(self, engine):
        self.engine = engine
        self.character_button = []
        self.sort_button = []
        self.sorting_button = []
        self.rarity_condition = ["6", "5", "4", "3", "2", "1"]
        self.type_condition = ["archer", "mage", "striker", "defender"]
        self.order_condition = "id"
        self.direction_condition = "ASC"
        self.operator_stuff = sort_data(
            self.order_condition,
            self.direction_condition,
            self.rarity_condition,
            self.type_condition,
        )
        self.sorting_commands = [
            "[√] rarity 6 star",
            "[√] rarity 5 star",
            "[√] rarity 4 star",
            "[√] rarity 3 star",
            "[√] rarity 2 star",
            "[√] rarity 1 star",
            "[√] type archer",
            "[√] type mage",
            "[√] type striker",
            "[√] type defender",
            "[_] order name",
            "[_] order level",
            "[_] order hp",
            "[_] order attack",
            "[_] order rarity",
            "[_] order type",
            "[_] order faction",
            "[√] order id",
            "[√] dir ASC",
            "[_] dir DESC",
        ]
        self.background = None
        self.button_spacing_x = 0.273
        self.button_spacing_y = 0.4
        self.button_start_positions = (-0.7279620853080568, 0.225)
        self.create_ui()

    def create_ui(self):
        self.create_bg()
        self.create_character_button()
        self.create_sort_button()

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
        text = Text(
            "Sort",
            parent=camera.ui,
            position=(0.8, 0.4),
            origin=(0, 0),
            color=color.rgba(0, 0, 0, 1),
            z=-0.1,
        )
        button.on_click = lambda: self.create_sorting_button()
        self.sort_button.append({"button": button, "text": text})

    def create_sorting_button(self):
        self.destroying_sort_buttons()
        y_index = 0
        x_index = 0
        previous_sort_type = None
        button = Entity(
            parent=camera.ui,
            position=(0, 0.4),
            model="quad",
            scale=(2, 0.2),
            color=color.rgba(0.6, 0.6, 0.6, 0.6),
            z=-0.1,
        )
        self.sorting_button.append({"button": button, "text": None})
        for commands in self.sorting_commands:
            check, sort_type, value = commands.split(maxsplit=2)
            if previous_sort_type != sort_type:
                y_index += 1
                if y_index / 2 != int(y_index / 2):
                    x_index = 0
                else:
                    x_index += 2
                button = Entity(
                    parent=camera.ui,
                    position=(-0.8 + (0.1 * x_index), 0.57 - (0.1 * ceil(y_index / 2))),
                    model="quad",
                    scale=(0.1, 0.05),
                    color=color.rgba(0.6, 0.6, 0.6, 0.6),
                    z=-0.1,
                )
                text = Text(
                    sort_type,
                    parent=camera.ui,
                    position=(-0.8 + (0.1 * x_index), 0.57 - (0.1 * ceil(y_index / 2))),
                    origin=(0, 0),
                    color=color.black,
                    z=-1,
                )
                self.sorting_button.append({"button": button, "text": text})
            else:
                x_index += 1
            button = Button(
                model="quad",
                parent=camera.ui,
                position=(-0.8 + (0.1 * x_index), 0.52 - (0.1 * ceil(y_index / 2))),
                scale=(0.1, 0.05),
                color=color.rgba(0.6, 0.6, 0.6, 0.6),
                z=-0.1,
            )
            button.on_click = lambda types=sort_type, values=value.split()[
                0
            ]: self.sorting(types, values)
            text = Text(
                f"{check} {value}",
                name=sort_type,
                parent=camera.ui,
                position=(-0.8 + (0.1 * x_index), 0.52 - (0.1 * ceil(y_index / 2))),
                origin=(0, 0),
                scale=0.8,
                color=color.black,
                z=-1,
            )
            self.sorting_button.append({"button": button, "text": text})
            previous_sort_type = sort_type

    def sorting(self, types, value):
        if types == "rarity":
            if value in self.rarity_condition:
                for i, stuffs in enumerate(self.sorting_commands):
                    stuff = stuffs.split()
                    if stuff[2] == value:
                        stuff[0] = "[_]"
                        self.sorting_commands[i] = " ".join(stuff)
                self.rarity_condition.remove(value)
            else:
                for i, stuffs in enumerate(self.sorting_commands):
                    stuff = stuffs.split()
                    if stuff[2] == value:
                        stuff[0] = "[√]"
                        self.sorting_commands[i] = " ".join(stuff)
                self.rarity_condition.append(value)
        elif types == "type":
            if value in self.type_condition:
                for i, stuffs in enumerate(self.sorting_commands):
                    stuff = stuffs.split()
                    if stuff[2] == value:
                        stuff[0] = "[_]"
                        self.sorting_commands[i] = " ".join(stuff)
                self.type_condition.remove(value)
            else:
                for i, stuffs in enumerate(self.sorting_commands):
                    stuff = stuffs.split()
                    if stuff[2] == value:
                        stuff[0] = "[√]"
                        self.sorting_commands[i] = " ".join(stuff)
                self.type_condition.append(value)
        elif types == "order":
            for i, stuffs in enumerate(self.sorting_commands):
                stuff = stuffs.split()
                if stuff[1] == types:
                    if stuff[2] == value:
                        stuff[0] = "[√]"
                        self.sorting_commands[i] = " ".join(stuff)
                    else:
                        stuff[0] = "[_]"
                        self.sorting_commands[i] = " ".join(stuff)
            self.order_condition = value
        else:
            for i, stuffs in enumerate(self.sorting_commands):
                stuff = stuffs.split()
                if stuff[1] == types:
                    if stuff[2] == value:
                        stuff[0] = "[√]"
                        self.sorting_commands[i] = " ".join(stuff)
                    else:
                        stuff[0] = "[_]"
                        self.sorting_commands[i] = " ".join(stuff)
            self.direction_condition = value
        self.operator_stuff = sort_data(
            self.order_condition,
            self.direction_condition,
            self.rarity_condition,
            self.type_condition,
        )
        self.destroying_character_buttons()
        self.destroying_sorting_buttons()
        self.create_sort_button()
        self.create_character_button()

    def destroying_sort_buttons(self):
        for item in self.sort_button:
            destroy(item["button"])
            if item["text"] is not None:
                destroy(item["text"])
        self.sort_button.clear()

    def destroying_sorting_buttons(self):
        for item in self.sorting_button:
            destroy(item["button"])
            if item["text"] is not None:
                destroy(item["text"])
        self.sorting_button.clear()

    def destroying_character_buttons(self):
        for stuff in self.character_button:
            destroy(stuff["button"])
            destroy(stuff["image"])
            destroy(stuff["level"])
        self.character_button.clear()

    def create_character_button(self):
        for i, items in enumerate(self.operator_stuff):
            character_name = items.get("name")
            character_level = items.get("level")
            x, y = self.button_start_positions
            button_bg = Button(
                parent=camera.ui,
                model="quad",
                position=(
                    x + (i // 2 * self.button_spacing_x),
                    y - (i % 2 * self.button_spacing_y) - 0.1,
                    -0.1,
                ),
                color=color.rgba(0.6, 0.6, 0.6, 0.6),
                scale=(0.2, 0.38),
            )
            button_bg.on_click = lambda c=items: self.running(c)
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
                    y - (i % 2 * self.button_spacing_y) - 0.1,
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
                    y - (i % 2 * self.button_spacing_y) - 0.25,
                ),
                origin=(0, 0),
                color=color.black,
                z=-1,
            )
            self.character_button.append(
                {"button": button_bg, "image": character_image, "level": level}
            )

    def running(self, c):
        # destoring the UI's so it doesnt get lag
        self.destroying_character_buttons()
        self.destroying_sort_buttons()
        self.destroying_sorting_buttons()
        # returning the character assets to the engine
        self.engine.character_button_clicked(c)


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
