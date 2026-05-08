import arcade
from pathlib import Path  # import path from pathlib
from players import PlayerChar

grid = 70
width = 15 * grid
height = 10 * grid
title = "Gamemaps Making"
scale = 1
speed = 5
gravity = 1 / 2
jump = 15
fontsize = 40 / 70
coin_scale = 0.5
path = Path(__file__).parent  # faster load handles for files


# level=[["level1.1.tmj","level1.2.tmj","level1.3.tmj"],["level2.1.tmj","level2.2.tmj","level2.3.tmj"],"level3.1.tmj","level3.2.tmj","level3.3.tmj"],["death_mode1.5.tmj","death_mode1.2.tmj","death_mode1.3.tmj","death_mode1.4.tmj","death_mode1.5.tmj"]]
class game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.ground = None
        self.obstacle = None
        self.text = [
            (
                (
                    (
                        "Press   or   to move around",
                        359.446,
                        339,
                        (255, 255, 255),
                        15.107,
                    ),
                    ("A    D", 446.167, 339, (0, 85, 255), 415.107),
                ),
                (
                    ("Click       to jump", 13.2053, 315.911, (255, 255, 255), 393.421),
                    ("space", 107.0, 315.5, (85, 255, 255), 141.5),
                ),
                (
                    (
                        "looks like your path is",
                        267.906882591,
                        566.352226721,
                        (255, 255, 255),
                        472.262483131,
                    ),
                    (
                        "blocked, hold      to",
                        267.906882591,
                        526.352226721,
                        (255, 255, 255),
                        472.262483131,
                    ),
                    (
                        "climb the ladder",
                        267.906882591,
                        486.352226721,
                        (255, 255, 255),
                        472.262483131,
                    ),
                    ("space", 465.868666667, 526.548833333, (85, 255, 255), 105.596),
                ),
            ),
            (
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
            ),
            (
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
            ),
            (
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
                (("", 0, 0, (0, 0, 0), 0), (" ", 0, 0, (0, 0, 0), 0)),
            ),
        ]
        self.main_menu_text = [
            ("level 1", width // 2 - 49, 500, (0, 0, 0)),
            ("level 2", width // 2 - 49, 427.5, (0, 0, 0)),
            ("level 3", width // 2 - 49, 355, (0, 0, 0)),
            ("death mode", width // 2 - 49, 282.5, (0, 0, 0)),
            ("quit", width // 2 - 49, 205, (0, 0, 0)),
        ]
        self.main_menu_line = []
        self.currentline = []
        self.text_prop = None
        self.prop = None
        self.title = None
        self.stair = None
        self.playerlist = None
        self.player = None
        self.can_climb = False
        self.player_speed = speed
        self.physic_engine = None
        self.bg_player = None
        self.in_level = False
        self.right_pressed = None
        self.left_pressed = None
        self.bg = []
        self.jump_sounds = arcade.load_sound("assets/sounds/jump_effect.mp3")
        self.bg_music = arcade.load_sound(str(path / "assets/sounds/main.mp3"))
        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        # self.bg_music=arcade.load_sound("assets/sounds/main.mp3")
        self.Button = None
        self.level = [
            [
                "assets/levels/level1.1.tmj",
                "assets/levels/level1.2.tmj",
                "assets/levels/level1.3.tmj",
            ],
            [
                "assets/levels/level2.1.tmj",
                "assets/levels/level2.2.tmj",
                "assets/levels/level2.3.tmj",
            ],
            [
                "assets/levels/level3.1.tmj",
                "assets/levels/level3.2.tmj",
                "assets/levels/level3.3.tmj",
            ],
            [
                "assets/levels/death_mode1.5.tmj",
                "assets/levels/death_mode1.2.tmj",
                "assets/levels/death_mode1.3.tmj",
                "assets/levels/death_mode1.4.tmj",
                "assets/levels/death_mode1.5.tmj",
            ],
        ]
        self.hp_sprite = arcade.load_texture("assets/picture/hp.png")
        self.level_progress = 1
        self.current_level = 1
        self.level_cap = [3, 3, 3, 5]
        self.current_coin = 0
        self.collected_coin = 0
        self.main_menu()

    def main_menu(self):
        self.screen_width = self.window.width
        self.screen_height = self.window.height
        self.life = 5
        if self.bg_player:
            arcade.stop_sound(self.bg_player)
        self.bg_player = arcade.play_sound(self.bg_music, 0.5, loop=True)
        self.life_text = arcade.Text("HP:", 10, height - 30, arcade.color.BLACK, 30)
        self.window.set_mouse_visible(False)
        self.level_progress = 1
        self.bg.clear()
        self.main_menu_line.clear()
        self.bg = []
        self.main_menu_line = []

        self.main_map = arcade.load_tilemap("assets/levels/main_menu.tmj")
        bg = self.main_map.sprite_lists["bg"]
        self.bg.append(bg)
        bg = self.main_map.sprite_lists["bg1"]
        self.bg.append(bg)
        bg = self.main_map.sprite_lists["bg2"]
        self.bg.append(bg)
        bg = self.main_map.sprite_lists["bg3"]
        self.bg.append(bg)
        bg = self.main_map.sprite_lists["bg4"]
        self.bg.append(bg)

        self.cursor_list = self.main_map.sprite_lists["Cursor"]
        self.cursor = self.cursor_list[0]
        self.Button = self.main_map.sprite_lists["Button"]

        for text, x, y, color in self.main_menu_text:
            sentence = arcade.Text(text, x, y, color, 22, font_name="MingLiU-ExtB")
            self.main_menu_line.append(sentence)

    def setup(self):
        self.collected_coin = 0
        # self.stuff=self.tilemap.spritelist.get("stuff",arcade.SpriteList())
        self.tilemap = arcade.load_tilemap(
            self.level[self.current_level - 1][self.level_progress - 1],
            layer_options={"ground": {"use_spatial_hash": True}},
        )
        self.background = self.tilemap.sprite_lists["background"]
        self.ground = self.tilemap.sprite_lists["ground"]
        self.stair = self.tilemap.sprite_lists["stairs"]
        self.prop = self.tilemap.sprite_lists["prop"]
        self.text_prop = self.tilemap.sprite_lists["text props"]
        self.obstacle = self.tilemap.sprite_lists["obstacles"]
        self.coinlist = self.tilemap.sprite_lists["coins"]
        self.players = arcade.SpriteList()
        self.player = PlayerChar()
        self.player.center_x = 40
        self.player.center_y = height // 3
        self.players.append(self.player)
        line = self.text[self.current_level - 1][self.level_progress - 1]
        for text in line:
            char, x, y, color, width = text
            lines = arcade.Text(char, x, y, color, 22, width, font_name="MingLiU-ExtB")
            self.currentline.append(lines)
        self.physic_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.ground, gravity_constant=gravity
        )
        self.title = arcade.Text(
            f"level {self.current_level}",
            self.screen_width // 2 - 70,
            self.screen_height - 40,
            arcade.color.WHITE,
            40,
        )
        self.in_level = True

    def on_draw(self):
        self.clear()
        if self.in_level:
            self.background.draw()
            self.ground.draw()
            if self.stair != None:
                self.stair.draw()
            self.prop.draw()
            self.text_prop.draw()
            for line in self.currentline:
                line.draw()
            if self.obstacle != None:
                self.obstacle.draw()
            self.coinlist.draw()
            self.title.draw()
            self.players.draw()
            for i in range(self.life):
                arcade.draw_texture_rect(
                    self.hp_sprite, arcade.XYWH(85 + 35 * i, height - 20, 30, 30)
                )
            self.life_text.draw()
        else:
            for back_ground in self.bg:
                back_ground.draw()
            self.Button.draw()
            for text in self.main_menu_line:
                text.draw()
        self.cursor_list.draw()

    def on_update(self, delta_time):
        if self.in_level:
            self.player.change_x = 0
            if self.left_pressed and not self.right_pressed:
                self.player.change_x = -speed
            if self.right_pressed and not self.left_pressed:
                self.player.change_x = speed
            self.player.update()
            self.players.update_animation()
            self.physic_engine.update()
            if self.player.center_x >= self.screen_width - self.player.width // 2:
                if self.level_progress <= self.level_cap[self.current_level - 1] - 1:
                    self.level_progress += 1
                    self.currentline.clear()
                    self.setup()
                else:
                    self.in_level = False
                    self.current_coin += self.collected_coin
                    self.main_menu()
                    self.currentline.clear()
            if arcade.check_for_collision_with_list(self.player, self.obstacle):
                self.life -= 1
                if self.life == 0:
                    self.window.show_view(self.window.game_over_view)
                self.setup()
            coin_hit_list = arcade.check_for_collision_with_list(
                self.player, self.coinlist
            )
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.collected_coin += 1
                arcade.play_sound(self.coin_sound)
            if arcade.check_for_collision_with_list(self.player, self.stair):
                self.can_climb = True
                self.physic_engine.gravity_constant = 0
            else:
                self.can_climb = False
                self.physic_engine.gravity_constant = 1 / 2
            self.can_jump = abs(self.player.velocity[1]) < 0.5
        else:
            self.current_level = 0
            for i, button in enumerate(self.Button):
                if arcade.check_for_collision(self.cursor, button):
                    button.alpha = 255
                    self.current_level = i + 1
                    self.in_collision_with_button = True
                else:
                    button.alpha = 255 / 2

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.in_level and self.current_level != 0:
            if self.current_level < 5:
                if button == arcade.MOUSE_BUTTON_LEFT:
                    self.setup()
            if self.current_level == 5:
                self.window.in_game_quit = True
                self.window.show_view(self.window.confirmation_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            if modifiers & arcade.key.MOD_SHIFT:
                self.player.change_x = -self.player_speed * 2
                self.left_pressed = True
                self.right_pressed = False
            else:
                self.player.change_x = -self.player_speed
                self.left_pressed = True
                self.right_pressed = False

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if modifiers & arcade.key.MOD_SHIFT:
                self.player.change_x = self.player_speed * 2
                self.left_pressed = False
                self.right_pressed = True
            else:
                self.player.change_x = self.player_speed
                self.left_pressed = False
                self.right_pressed = True

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.can_climb:
                self.player.change_y = self.player_speed
            elif self.physic_engine.can_jump():
                self.player.change_y = 12
                arcade.play_sound(self.jump_sounds)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.can_climb:
                self.player.change_y = -self.player_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.MOD_SHIFT:
            self.player_speed = 5
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0
            self.right_pressed = False
            self.left_pressed = False
        if self.can_climb:
            if key in (
                arcade.key.SPACE,
                arcade.key.W,
                arcade.key.S,
                arcade.key.UP,
                arcade.key.DOWN,
            ):
                self.player.change_y = 0
