import arcade

font = 20


class Episode(arcade.View):
    def __init__(self, path):
        super().__init__()
        self.count = 1
        self.texts = []
        self.main_map = arcade.load_tilemap(path)
        self.bg = self.main_map.sprite_lists["episode_bg"]
        self.items = self.main_map.sprite_lists["items"]
        for item in self.items:
            if item.properties["id"] <= self.count:
                item.visible = True
                print(item.properties)
                if (
                    item.properties["type"] == "main"
                    or item.properties["type"] == "sub"
                ):
                    text = arcade.Text(
                        item.properties["name"],
                        item.center_x - len(item.properties["name"]) * 7,
                        item.center_y - font // 2,
                        arcade.color.WHITE,
                        font,
                    )
                    self.texts.append(text)
            else:
                item.visible = False

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.items.draw()
        if self.texts:
            for text in self.texts:
                text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.count += 1
        self.refresh()

    def refresh(self):
        self.texts.clear()
        for item in self.items:
            if item.properties["id"] <= self.count:
                item.visible = True
                print(item.properties)
                if (
                    item.properties["type"] == "main"
                    or item.properties["type"] == "sub"
                ):
                    text = arcade.Text(
                        item.properties["name"],
                        item.center_x - len(item.properties["name"]) * 7,
                        item.center_y - font // 2,
                        arcade.color.WHITE,
                        font,
                    )
                    self.texts.append(text)
            else:
                item.visible = False


window = arcade.Window(1920, 1080, "Testing")
window.game_view = Episode("assets/tile/episode_1.tmj")
window.show_view(window.game_view)
arcade.run()
