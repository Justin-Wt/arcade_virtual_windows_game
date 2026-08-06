from ursina import *
from arkmania_episode_engine import Picked_Episode
from datamanager import Data_Manager


class Episode:
    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.buttons = self.create_buttons()
        self.backgrounds = []
        self.episode_button = []
        self.episodes = []
        self.content = None
        self.scroll_x = 0
        self.panel = None
        self.filename = "Arkmania.JSON"
        self.data_manager = Data_Manager(self.filename)
        self.show_episode()

        self.input_entity = Entity()
        self.update_entity = Entity()
        self.input_entity.input = self.input
        self.update_entity.update = self.update

    def create_buttons(self):
        leave_button = Button(
            text="<-",
            parent=camera.ui,
            model="quad",
            position=(-0.82, 0.475),
            scale=(0.15, 0.05),
            color=color.red,
        )
        leave_button.on_click = lambda: self.leaving()
        return [leave_button]

    def leaving(self):
        self.destroy_ui()
        self.main_menu.return_to_main_menu()

    def destroy_ui(self):
        for button in self.buttons:
            destroy(button)
        for background in self.backgrounds:
            destroy(background)
        for button in self.episode_button:
            destroy(button)
        if self.panel:
            destroy(self.panel)
            self.panel = None
        self.episodes.clear()
        self.buttons.clear()
        self.backgrounds.clear()
        self.episode_button.clear()

    def show_ui(self):
        self.buttons = self.create_buttons()

    def run_to_episode(self, name):
        self.destroy_ui()
        episode_file = name.replace(" ", "_")
        Picked_Episode(
            path=f"assets/tile/{episode_file}.tmj", episode=name, episode_pick=self
        )

    def return_to_episode_pick(self):
        self.show_ui()
        self.show_episode()

    def show_episode(self):
        datas = self.data_manager.open_file("Episodes")
        for episode, _ in datas.items():
            self.episodes.append(episode)
        self.panel = Entity(
            parent=camera.ui,
            name="panel",
            model="quad",
            color=color.rgba(0, 0, 0, 0.45),
            scale=(2, 0.4),
            position=(0, -0.3),
            collider=None,
        )
        self.content = Entity(
            parent=self.panel,
            scale=(1 / 2, 1 / 0.4),  # (0.5, 2.5)
        )
        for i, episode in enumerate(self.episodes):
            button = Button(
                episode,
                name="episode",
                parent=self.content,
                texture=f"assets/UI's/episodes/{episode}.png",
                origin=(0, 0),
                scale=(0.35, 0.35),
                text_size=2,
                position=((-0.3 + (i * 0.25)) * 2, 0),
                color=color.white,
            )
            button.on_click = lambda episode_name=episode: self.run_to_episode(
                episode_name
            )
            self.episode_button.append(button)

    def mouse_over_panel(self):
        return -1 <= mouse.x <= 1 and -0.5 <= mouse.y <= -0.1

    def input(self, key):
        if self.mouse_over_panel():
            if key == "scroll up":
                self.scroll_x += 0.02
            elif key == "scroll down":
                self.scroll_x -= 0.02
            self.scroll_x = min(self.scroll_x, 0.2)
            self.content.x = self.scroll_x

    def update(self):
        for button in self.episode_button:
            left_distance = button.world_x - (-18.5)
            right_distance = 18.25 - button.world_x
            distance = min(left_distance, right_distance)
            alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0
            button.alpha = alpha
            button.text_entity.alpha = alpha
