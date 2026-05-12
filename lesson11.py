import arcade
import os
from main_game import game
import win32con
import win32gui

grid = 70
width = 15 * grid
height = 10 * grid
filepath = os.path.dirname(os.path.abspath(__file__))
os.chdir(filepath)
title = "game screen example"
scale = 1
speed = 5
gravity = 1 / 2
jump = 15
fontsize = 40 / 70
coin_scale = 0.5


class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()
        hwnd = win32gui.FindWindow(None, title)
        # Set window as topmost
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "This is Start Game Screen",
            width // 2,
            height // 2,
            arcade.color.WHITE,
            font_size=35,
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            "Click to Continue",
            width // 2,
            height // 2 - 50,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(self.window.game_view)

    def on_key_press(self, key: int, modifiers):
        if key == arcade.key.M:
            self.window.set_fullscreen(True)
        if key == arcade.key.N:
            self.window.set_fullscreen(False)


class GameOverScreen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Do you want to restart?",
            width // 2,
            height // 2,
            arcade.color.WHITE,
            font_size=35,
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            "Type 'R' to restart or 'Q' to quit",
            width // 2,
            height // 2 - 50,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, key: int, modifiers):
        if key == arcade.key.M:
            self.window.set_fullscreen(True)
        if key == arcade.key.N:
            self.window.set_fullscreen(False)
        if key == arcade.key.R:
            self.window.game_view.main_menu()
            self.window.show_view(self.window.game_view)
        if key == arcade.key.Q:
            self.window.show_view(self.window.confirmation_view)


class ConfirmationScreen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Are you sure you want to quit?",
            width // 2,
            height // 2,
            arcade.color.WHITE,
            font_size=35,
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            "Type 'Y' to quit or 'N' to Continue",
            width // 2,
            height // 2 - 100,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, key: int, modifiers):
        if key == arcade.key.M:
            self.window.set_fullscreen(True)
        if key == arcade.key.N:
            self.window.set_fullscreen(False)
        if key == arcade.key.Y:
            arcade.close_window()
        if key == arcade.key.N:
            if self.window.in_game_quit == True:
                self.window.game_view.main_menu()
                self.window.show_view(self.window.game_view)
                self.window.in_game_quit = False
            else:
                self.window.show_view(self.window.start_view)


if __name__ == "__main__":
    window = arcade.Window(width, height, title)
    start_view = StartScreen()
    game_view = game()
    game_over_view = GameOverScreen()
    confirmation_view = ConfirmationScreen()

    # store references
    window.in_game_quit = False
    window.start_view = start_view
    window.game_view = game_view
    window.game_over_view = game_over_view
    window.confirmation_view = confirmation_view
    window.show_view(start_view)
    arcade.run()
