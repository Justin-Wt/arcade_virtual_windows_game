from ursina import *
from collections import deque
from direct.actor.Actor import Actor
from datamanager import Data_Manager
import random

# adding win screen and lose screen with character and rewards


class Game:
    def __init__(
        self,
        filename,
        level,
        episode,
        sub=False,
        condition=[],
        current_episode="Episode 1",
        character="slot 1",
    ):
        self.episode = episode
        self.current_episode = current_episode
        self.buttons = []
        self.end_ui = []
        self.indicator_list = []
        self.pathing = False
        self.indicator_time = 0
        self.current_base_hp = 10
        self.base_hp = 10
        self.global_timer = 0
        self.deployed = 0
        self.level = level
        self.hovered_tile = None
        self.rotating = False
        self.showing_range = False
        self.dragging = False
        self.squad_data_manager = Data_Manager("Arkmania_Squad.JSON")
        self.data_manager = Data_Manager(filename)
        for e in scene.entities:
            if isinstance(e, EditorCamera):
                self.camera = e
        self.grid, self.tiles = self.tile_maker(self.level)
        self.end = False
        self.first_clear = False
        self.star = 0
        self.speed = 1
        self.sub = sub
        self.condition = condition
        self.Character_Name = self.getting_character_name(character)
        self.reward_tags = []

        self.input_entity = Entity()
        self.update_entity = Entity()
        self.player_manager = PlayerManager(self)
        self.enemy_manager = EnemyManager(self)
        self.wave_manager = WaveManager(self)
        self.ui_manager = UIManager(self)
        self.setup_ui()
        self.input_entity.input = self.input
        self.update_entity.update = self.update

    def setup_ui(self):
        self.ui_manager.create_hp_text(self.current_base_hp, self.base_hp)
        self.ui_manager.draw_player_button()
        self.ui_manager.draw_speed_up_button()
        self.ui_manager.draw_restart_button()

    def mouse_hover_loot_panel(self):
        return -1 <= mouse.x <= 1 and -0.375 <= mouse.y <= -0.225

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
                    index=index,
                    model=f"assets/3d/cube_structure.obj" if index < 3 else "cube",
                    scale=(1, (0.1 + height if height > 0 else 0.1), 1),
                    position=(x, height / 2, z),
                    texture=(
                        f"assets/3d/ground_texture_{self.current_episode}.png"
                        if index == 0
                        else (
                            f"assets/3d/land_texture_{self.current_episode}.png"
                            if index == 1
                            else (
                                f"assets/3d/enemy_spawn_texture.png"
                                if index == 2
                                else "white_cube"
                            )
                        )
                    ),
                    color=color.rgba(0, 0, 0.8, 0.85) if index == 3 else color.white,
                    collider="box",
                )
                tiles.append(tile)
                if index > 0:
                    tile = Entity(
                        index=index if index < 2 else 9,
                        model=f"assets/3d/cube_structure.obj",
                        scale=(1, 0.1, 1),
                        position=(x, -0.1, z),
                        texture=f"assets/3d/ground_texture_{self.current_episode}.png",
                        color=color.gray,
                        collider="box",
                    )
                    tiles.append(tile)

        return grid, tiles

    def rotation(self, attack_range):
        return [list(row) for row in zip(*attack_range[::-1])]

    def getting_character_name(self, character):
        chars = []
        character_data = self.squad_data_manager.open_file(character)
        for name in character_data:
            if name != "none":
                chars.append(name)
        return chars

    def restarting(self):
        if self.player_manager.players:
            for player in self.player_manager.players:
                destroy(player)
            self.player_manager.players.clear()
        if self.enemy_manager.enemies:
            for enemy in self.enemy_manager.enemies:
                destroy(enemy)
            self.enemy_manager.enemies.clear()
        if self.enemy_manager.spawning_enemies:
            for spawn in self.enemy_manager.spawning_enemies:
                destroy(spawn)
            self.enemy_manager.spawning_enemies.clear()
        if self.end:
            for ui in self.end_ui:
                destroy(ui)
            self.end_ui.clear()
        self.wave_manager.wave_count = 0
        self.global_timer = 0
        self.enemy_manager.spawning_timer = 0
        self.current_base_hp = 10
        self.base_hp = 10
        self.player_manager.character_spawning = False
        self.player_manager.character_spawned_player = None
        self.hovered_tile = None
        self.rotating = False
        self.showing_range = False
        self.dragging = False
        self.end = False
        self.win = False
        self.pathing = False
        self.indicator_list.clear()
        self.indicator_time = 0
        destroy(self.ui_manager.hp_text)
        self.ui_manager.create_hp_text(self.current_base_hp, self.base_hp)

    def find_center(self, attack_range):
        for z in range(len(attack_range)):
            for x in range(len(attack_range[0])):
                if attack_range[z][x] == 2:
                    center_x = x
                    center_z = z
        offset_x = -center_x
        offset_z = -center_z
        return offset_x, offset_z

    def get_rotated_attack_range(self, entity):
        if entity.direction == "Front":
            attack_range = self.rotation(entity.attack_range)
        elif entity.direction == "Left":
            attack_range = entity.attack_range
        elif entity.direction == "Right":
            attack_range = self.rotation(self.rotation(entity.attack_range))
        elif entity.direction == "Back":
            attack_range = self.rotation(
                self.rotation(self.rotation(entity.attack_range))
            )
        return attack_range

    def attack(self, attacker, target, target_lists):
        if attacker.can_attack:
            target.hp -= attacker.damage
            if target.hp <= 0:
                self.removing(target, target_lists)
            attacker.can_attack = False
            attacker.already_attack = True

    def removing(self, target, target_lists):
        if isinstance(target, Enemy):
            if target.blocked:
                target.blocking_player.blocking -= 1
            target_lists.remove(target)
            destroy(target)
        elif isinstance(target, Player):
            for enemy in self.enemy_manager.enemies:
                if enemy.blocking_player == target:
                    enemy.blocked = False
            target_lists.remove(target)
            destroy(target)

    def check_attack(self, attacker_list, target_lists):
        for attacker in attacker_list:
            attack_range = self.get_rotated_attack_range(attacker)
            offset_x, offset_z = self.find_center(attack_range)
            for z in range(offset_z, len(attack_range) + offset_z):
                for x in range(offset_x, len(attack_range[0]) + offset_x):
                    if attack_range[z - offset_z][x - offset_x] > 0:
                        for target in target_lists:
                            if (
                                target.position.x < attacker.position[0] + x + 0.5
                                and target.position.x > attacker.position[0] + x - 0.5
                            ):
                                if (
                                    target.position.z < attacker.position[2] + z + 0.5
                                    and target.position.z
                                    > attacker.position[2] + z - 0.5
                                ):
                                    if isinstance(target, Player):
                                        if target.layer == 1:
                                            if attacker.can_attack_units_on_high_ground:
                                                self.attack(
                                                    attacker, target, target_lists
                                                )
                                        elif target.layer == 0 and attacker.blocked:
                                            self.attack(attacker, target, target_lists)
                                    else:
                                        self.attack(attacker, target, target_lists)

    def update_cube_color(self):
        for cube in self.tiles:
            if (
                mouse.world_point.x < cube.x + 0.5
                and mouse.world_point.x > cube.x - 0.5
                and mouse.world_point.z < cube.z + 0.5
                and mouse.world_point.z > cube.z - 0.5
            ):
                self.hovered_tile = cube
                if not self.player_manager.character_spawning:
                    self.hovered_tile.color = color.red
            if self.player_manager.character_spawning:
                if (
                    cube.index == self.player_manager.character_spawned_player.layer
                    and cube == self.hovered_tile
                ):
                    cube.color = color.red
                elif cube.index == self.player_manager.character_spawned_player.layer:
                    cube.color = color.rgba(0.8, 0.8, 0.8, 1)
                elif cube.index == 3:
                    cube.color = color.rgba(0, 0, 0.8, 0.85)
                elif cube.index == 2:
                    cube.color = color.rgba(0.8, 0, 0, 0.85)
                else:
                    cube.color = color.gray
            else:
                if cube.index == 3:
                    cube.color = color.rgba(0, 0, 0.8, 0.85)
                elif cube.index == 2:
                    cube.color = color.rgba(0.8, 0, 0, 0.85)
                else:
                    cube.color = color.gray

    def cleanup(self):
        self.ui_manager.cleanup()
        if self.player_manager.character_spawned_player:
            destroy(self.player_manager.character_spawned_player)
            self.player_manager.character_spawned_player = None
        for tile in self.tiles:
            destroy(tile)

        for button in self.buttons:
            destroy(button)

        for player in self.player_manager.players:
            destroy(player)

        for enemy in self.enemy_manager.enemies:
            destroy(enemy)

        for enemy in self.enemy_manager.spawning_enemies:
            destroy(enemy)

        for ui in self.end_ui:
            destroy(ui)

        destroy(self.ui_manager.hp_text)

        destroy(self.input_entity)
        destroy(self.update_entity)

    def calculate_star(self, deployed, base_hp):
        star = 0
        if "victory" in self.condition:
            star += 1
        if "under_10_units" in self.condition:
            if deployed <= 10:
                star += 1
        if "no_hp_loss" in self.condition:
            if base_hp == 10:
                star += 1
        return star

    def main_reward(self):
        self.reward_tags.append("main")

    def basic_reward(self):
        self.reward_tags.append("basic")

    def special_reward(self):
        self.reward_tags.append("special")

    def calculating_rewards(self):
        self.win = True
        self.star = self.calculate_star(self.deployed, self.current_base_hp)
        if self.star == 3:
            self.special_reward()
        if not self.episode.level_data.get(self.level, {}).get("cleared"):
            self.first_clear = True
            self.main_reward()
        if self.star > 0:
            self.basic_reward()
        self.ui_manager.end_screen("You Win")

    def input(self, key):
        if self.mouse_hover_loot_panel() and self.ui_manager.loot_panel:
            if key == "scroll down" or key == "scroll up":
                self.camera.rotation_speed = 0
                self.camera.move_speed = 0
                self.camera.zoom_speed = 0
                if key == "scroll up":
                    self.ui_manager.loot_panel_scroll_x += 0.02
                elif key == "scroll down":
                    self.ui_manager.loot_panel_scroll_x -= 0.02
            else:
                self.camera.rotation_speed = 200
                self.camera.move_speed = 10
                self.camera.zoom_speed = 1.25
            self.ui_manager.loot_panel_scroll_x = min(
                self.ui_manager.loot_panel_scroll_x, 0.2
            )
            self.ui_manager.loot_content.x = self.ui_manager.loot_panel_scroll_x
        if key == "left mouse up" and self.end:
            self.episode.return_to_episode(
                win=self.win,
                sub=self.sub,
                level=self.level,
                first_clear=self.first_clear,
                star=self.star,
                rewards=self.reward_tags,
            )
            self.cleanup()
        if key == "left mouse up" and self.dragging:
            preview = self.player_manager.character_spawned_player

            if preview not in self.player_manager.players:
                self.player_manager.players.append(preview)
                self.deployed += 1

            self.player_manager.character_spawned_player = None

            self.dragging = False
            self.rotating = False
            self.showing_range = False
        if key == "left mouse down" and self.rotating == True:
            self.dragging = True
        if self.player_manager.character_spawning and self.hovered_tile:
            if (
                self.hovered_tile.index
                != self.player_manager.character_spawned_player.layer
            ):
                return
            if key == "left mouse down":
                for player in self.player_manager.players:
                    if player.position == (
                        self.hovered_tile.position.x,
                        (
                            self.hovered_tile.index
                            if self.hovered_tile.index > 0
                            else -0.05
                        ),
                        self.hovered_tile.position.z,
                    ):
                        return
                self.player_manager.character_spawned_player.position = (
                    self.hovered_tile.x,
                    (self.hovered_tile.index if self.hovered_tile.index > 0 else -0.05),
                    self.hovered_tile.z,
                )
                self.player_manager.character_spawning = False
                self.rotating = True
                self.showing_range = True

    def update(self):
        self.global_timer += time.dt * self.speed
        self.enemy_manager.update()
        if self.ui_manager.loot_panel:
            for button in self.ui_manager.loot_button:
                left_distance = button.world_x - (-18.5)
                right_distance = 12.25 - button.world_x
                distance = min(left_distance, right_distance)
                alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0
                button.alpha = alpha
            for frame in self.ui_manager.loot_frame:
                left_distance = frame.world_x - (-18.5)
                right_distance = 12.25 - frame.world_x
                distance = min(left_distance, right_distance)
                alpha = clamp(abs(distance) / 1, 0, 1) if distance >= 0 else 0
                frame.alpha = alpha

        if self.enemy_manager.enemies and self.player_manager.players:
            for player in self.player_manager.players:
                self.ui_manager.update_hp_bar(player)
            for enemy in self.enemy_manager.enemies:
                self.ui_manager.update_hp_bar(enemy)
            self.check_attack(self.player_manager.players, self.enemy_manager.enemies)
            self.check_attack(self.enemy_manager.enemies, self.player_manager.players)
        if self.current_base_hp == 0 and not self.end:
            self.ui_manager.end_screen("You Lose")
        if not mouse.world_point:
            return
        self.update_cube_color()

        self.player_manager.update()


class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.spawning_enemies = []
        self.spawning_timer = 0
        self.blocking_player = None

    def enemy_ai(self, gate):
        starts = []
        for cube in self.game.tiles:
            if cube.index == 3:
                goal = (cube.world_position.x, cube.world_position.z)
            elif cube.index == 2:
                starts.append((cube.world_position.x, cube.world_position.z))
        queue = deque([(starts[gate], [])])
        visited = set()
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        while queue:
            (x, z), path = queue.popleft()
            if (x, z) in visited:
                continue
            visited.add((x, z))
            path = path + [(x, z)]
            if (x, z) == goal:
                return starts[gate], goal, path
            for dx, dz in directions:
                nx = x + dx
                nz = z + dz
                if 0 <= nx < len(self.game.grid[0]) and 0 <= nz < len(self.game.grid):
                    if self.game.grid[int(nz)][int(nx)] != 1:
                        queue.append(((nx, nz), path))

    def update(self):
        self.checking_enemy_spawn(self.game.level)
        if self.spawning_enemies:
            self.spawning_timer += time.dt * self.game.speed
            self.update_spawn()
        if self.enemies:
            self.checking_paths()
            self.update_attack()

    def update_attack(self):
        for enemy in self.enemies:
            enemy.timer -= time.dt * self.game.speed
            if enemy.timer <= 0:
                enemy.can_attack = True
            if enemy.already_attack:
                enemy.timer = enemy.cooldown
                enemy.already_attack = False

    def update_spawn(self):
        if self.spawning_enemies:
            if self.spawning_timer > 1:
                enemy = self.spawning_enemies[0]
                self.enemies.append(enemy)
                del self.spawning_enemies[0]
                self.spawning_timer = 0

    def checking_enemy_spawn(self, level=1):
        waves = self.game.data_manager.open_file(
            "Episodes", self.game.current_episode, f"Level {level}", "waves"
        )
        if self.game.wave_manager.wave_count < len(waves):
            current_wave = waves[self.game.wave_manager.wave_count]
            wave_time = current_wave["time"]
            if self.game.global_timer > wave_time - 1:
                if self.game.pathing == False:
                    self.game.ui_manager.show_indicator(
                        level, self.game.wave_manager.wave_count + 1
                    )
                else:
                    self.game.ui_manager.animate_indicator(
                        level, self.game.wave_manager.wave_count + 1
                    )
            if self.game.global_timer > wave_time:
                self.game.wave_manager.enemy_spawn_per_waves(
                    level, self.game.wave_manager.wave_count + 1
                )
                self.game.pathing = False
                self.game.wave_manager.wave_count += 1
        if self.game.wave_manager.wave_count == len(waves):
            if (
                not self.enemies
                and not self.spawning_enemies
                and self.game.current_base_hp > 0
                and not self.game.end
            ):
                self.game.calculating_rewards()

    def checking_paths(self):
        for enemy in self.enemies:
            if enemy.path:
                next_position = enemy.path[0]
                if enemy.blocked == False:
                    speed = min(time.dt * self.game.speed, 0.2)
                    target = Vec3(next_position[0], 0.5, next_position[1])
                    dir_x = next_position[0] - enemy.position.x
                    dir_z = next_position[1] - enemy.position.z
                    if abs(dir_x) > abs(dir_z):
                        enemy.direction = "Back" if dir_x > 0 else "Front"
                    else:
                        enemy.direction = "Left" if dir_z > 0 else "Right"
                    enemy.position += (target - enemy.position).normalized() * speed
                    if distance(enemy.position, target) < max(0.05, speed):
                        enemy.position = target
                        enemy.path.pop(0)
                    if (
                        enemy.position.x == enemy.goal[0]
                        and enemy.position.z == enemy.goal[1]
                    ):
                        self.game.current_base_hp -= 1
                        destroy(self.game.ui_manager.hp_text)
                        self.game.ui_manager.hp_text = Text(
                            text=f"{self.game.current_base_hp}/{self.game.base_hp}",
                            position=(-0.8, 0.45),  # UI coordinates
                            scale=2,
                        )
                        if enemy.blocked:
                            enemy.blocking_player.blocking -= 1
                        self.enemies.remove(enemy)
                        destroy(enemy)
                for player in self.game.player_manager.players:
                    if (
                        next_position == (player.position.x, player.position.z)
                        and player.blocking < player.block_limit
                        and enemy.blocked == False
                        and player.can_block
                    ):
                        player.blocking += 1
                        enemy.blocked = True
                        enemy.blocking_player = player
                    elif enemy.blocked:
                        continue


class PlayerManager:
    def __init__(self, game):
        self.game = game
        self.players = []
        self.character_spawning = False
        self.character_spawned_player = None

    def update(self):
        self.update_rotation()
        self.update_spawn_position()
        self.update_hover()
        self.update_spawn_range()

    def update_rotation(self):
        if self.game.rotating and self.game.dragging:
            dx = mouse.world_point.x - self.character_spawned_player.x
            dz = mouse.world_point.z - self.character_spawned_player.z
            if abs(dx) > abs(dz):
                if dx > 0:
                    self.character_spawned_player.direction = "Back"
                    self.character_spawned_player.setH(90)
                else:
                    self.character_spawned_player.direction = "Front"
                    self.character_spawned_player.setH(270)
            else:
                if dz > 0:
                    self.character_spawned_player.direction = "Left"
                    self.character_spawned_player.setH(180)
                else:
                    self.character_spawned_player.direction = "Right"
                    self.character_spawned_player.setH(0)

    def update_spawn_position(self):
        if self.character_spawning:
            self.character_spawned_player.position = (
                mouse.world_point.x,
                0.5,
                mouse.world_point.z,
            )

    def update_hover(self):
        if self.players:
            for player in self.players:
                if (
                    mouse.world_point.x < player.world_position.x + 0.5
                    and mouse.world_point.x > player.world_position.x - 0.5
                ):
                    if (
                        mouse.world_point.z < player.world_position.z + 0.5
                        and mouse.world_point.z > player.world_position.z - 0.5
                    ):
                        self.show_range(player)
                else:
                    player.color = color.white
                self.game.ui_manager.update_hp_bar(player)
                player.timer -= time.dt * self.game.speed
                if player.timer <= 0:
                    player.can_attack = True
                if player.already_attack:
                    player.timer = player.cooldown
                    player.already_attack = False

    def update_spawn_range(self):
        if self.game.showing_range:
            self.show_range(self.character_spawned_player)

    def character_spawn(self, name):
        if self.character_spawning and self.character_spawned_player:
            destroy(self.character_spawned_player)
            self.character_spawned_player = None

        self.character_spawning = True
        data = self.game.data_manager.open_file("Characters", name)
        player_mdl = data["model"]
        player_range = data["attack_range"]
        player_tipe = data["type"]
        player_cool = data["cooldown"]
        player_dmg = data["damage"]
        player_blk_lim = data["block_limit"]
        player_hp = data["hp"]
        player_layer = data["layer"]
        self.character_spawning = True
        self.character_spawned_player = Player(
            collider="box",
            attack_range=player_range,
            direction="Front",
            type=player_tipe,
            position=(mouse.world_point.x, 0.5, mouse.world_point.z),
            already_attack=False,
            can_attack=False,
            cooldown=player_cool,
            timer=0,
            damage=player_dmg,
            max_hp=player_hp,
            blocking=0,
            block_limit=player_blk_lim,
            hp=player_hp,
            layer=player_layer,
            can_block=True if player_layer == 0 else False,
        )
        self.character_spawned_player.background_bar = Entity(
            parent=self.character_spawned_player,
            model="quad",
            color=color.rgba(0, 0, 0, 0.5),
            position=(0, 1.7, 0),
            scale=(1.5, 0.1),
            billboard=True,
        )
        self.character_spawned_player.hp_bar = Entity(
            parent=self.character_spawned_player.background_bar,
            model="quad",
            color=(color.green),
            position=(-0.5, 0, 0),
            origin=(-0.5, 0, 0),
            scale=(1, 1),
        )
        self.character_spawned_player.setH(-90)
        self.character_spawned_player.actor = Actor(player_mdl)
        self.character_spawned_player.actor.reparentTo(self.character_spawned_player)
        # calculate height limit
        min_pt, max_pt = self.character_spawned_player.actor.getTightBounds()
        target_height = 2
        current_height = max_pt.y - min_pt.y
        scale = target_height / current_height
        self.character_spawned_player.actor.setScale(scale)

    def show_range(self, player):
        attack_range = self.game.get_rotated_attack_range(player)
        for z in range(len(attack_range)):
            for x in range(len(attack_range[0])):
                if attack_range[z][x] == 2:
                    center_x = x
                    center_z = z
        offset_x = -center_x
        offset_z = -center_z
        for z in range(offset_z, len(attack_range) + offset_z):
            for x in range(offset_x, len(attack_range[0]) + offset_x):
                if attack_range[z - offset_z][x - offset_x] > 0:
                    for cube in self.game.tiles:
                        if (
                            cube.world_position.x < player.position[0] + x + 0.5
                            and cube.world_position.x > player.position[0] + x - 0.5
                        ):
                            if (
                                cube.world_position.z < player.position[2] + z + 0.5
                                and cube.world_position.z > player.position[2] + z - 0.5
                            ):
                                cube.color = color.red


class WaveManager:
    def __init__(self, game):
        self.game = game
        self.wave_count = 0

    def enemy_spawn_per_waves(self, level, wave):
        datas = self.game.data_manager.open_file(
            "Episodes", self.game.current_episode, f"Level {level}", "waves"
        )
        wave_data = datas[wave - 1]
        for data in wave_data["spawns"]:
            e_type = data["enemy_type"]
            amounts = data["amount"]
            gates = data["gates"]
            enemy_datas = self.game.data_manager.open_file("Enemies", e_type)
            enemy_attack_range = enemy_datas["attack_range"]
            enemy_type = enemy_datas["type"]
            enemy_cooldown = enemy_datas["cooldown"]
            enemy_damage = enemy_datas["damage"]
            enemy_hp = enemy_datas["hp"]
            enemy_layer = enemy_datas["layer"]
            ai = self.game.enemy_manager.enemy_ai(gates - 1)
            for i in range(amounts):
                enemy = Enemy(
                    model="cube",
                    scale=(1, 1, 1),
                    position=(ai[0][0], 0.5, ai[0][1]),
                    texture="white_cube",
                    color=color.black,
                    collider="box",
                    direction="Front",
                    attack_range=enemy_attack_range,
                    goal=ai[1],
                    path=ai[2].copy(),
                    enemy_type=enemy_type,
                    weight=1,
                    cooldown=enemy_cooldown,
                    max_hp=enemy_hp,
                    hp=enemy_hp,
                    damage=enemy_damage,
                    layer=enemy_layer,
                    can_attack_units_on_high_ground=(
                        False if enemy_type == "melee" else True
                    ),
                )
                enemy.background_bar = Entity(
                    parent=enemy,
                    model="quad",
                    color=color.rgba(0, 0, 0, 0.5),
                    position=(0, 1.7, 0),
                    scale=(1.5, 0.1),
                    billboard=True,
                )
                enemy.hp_bar = Entity(
                    parent=enemy.background_bar,
                    model="quad",
                    color=(color.green),
                    position=(-0.5, 0, 0),
                    origin=(-0.5, 0, 0),
                    scale=(1, 1),
                )
                self.game.enemy_manager.spawning_enemies.append(enemy)


class UIManager:
    def __init__(self, game):
        self.game = game
        self.hp_text = None
        self.loot = []
        self.loot_frame = []
        self.loot_button = []
        self.loot_panel_scroll_x = 0
        self.speed_button = None
        self.loot_panel = None
        self.restart_button = None
        self.loot_content = None

    def create_hp_text(self, current_hp, max_hp):
        self.hp_text = Text(
            text=f"{current_hp}/{max_hp}",
            position=(-0.8, 0.45),  # UI coordinates
            scale=2,
        )

    def end_screen(self, text):
        self.game.end = True
        background = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgba(0, 0, 0, 0),
            scale=(2, 1),
            z=1,
        )
        background.animate_color(color.rgba(0, 0, 0, 0.7), duration=0.5)
        txt = Text(text, origin=(0, 0), scale=3, color=color.lime)
        self.game.end_ui = [background, txt]
        if self.game.win:
            self.show_reward(self.game.reward_tags)

    def cleanup(self):
        for button in self.loot_button:
            destroy(button)
        for frame in self.loot_frame:
            destroy(frame)
        self.loot_button.clear()
        self.loot_frame.clear()
        self.loot.clear()
        destroy(self.restart_button)
        if self.loot_content:
            destroy(self.loot_content)
            self.loot_content = None
        if self.loot_panel:
            destroy(self.loot_panel)
            self.loot_panel = None
        if self.speed_button:
            destroy(self.speed_button)
            self.speed_button = None

    def draw_restart_button(self):
        self.restart_button = Button(
            model="quad", scale=(0.1, 0.1), position=(-0.9, 0.5), color=color.red
        )
        self.restart_button.on_click = self.game.restarting

    def show_reward(self, reward):
        datas = self.game.data_manager.open_file(
            "Episodes", self.game.current_episode, f"Level {self.game.level}", "rewards"
        )
        for loot_types, lootable in datas.items():
            if loot_types not in reward:
                continue
            for loots in lootable:
                loot_type = loot_types
                loot = loots.get("item")
                chance = loots.get("chance", 1)
                min_amount = loots.get("min_amount", 1)
                max_amount = loots.get("max_amount", 1)
                steps = loots.get("steps", 1)
                roll = random.randint(1, 100)
                if roll <= chance:
                    amount = random.randrange(min_amount, max_amount + 1, steps)
                    self.loot.append([loot_type, loot, amount])
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
        for i, (loot_type, loot, amount) in enumerate(self.loot):
            button = Button(
                name="loot",
                color=color.white,
                parent=self.loot_content,
                origin=(0, 0),
                scale=(0.4, 0.4),
                texture=f"assets/picture/items/{loot}.png",
                position=(0.3 + (i * 0.625), 0),
            )
            frame = Entity(
                name="frame",
                model="quad",
                parent=self.loot_content,
                color=color.white,
                origin=(0, 0),
                scale=(0.6, 0.6),
                texture=f"assets/picture/items/{loot_type}_frame.png",
                position=(0.3 + (i * 0.625), 0, -0.01),
            )
            # button.on_click = lambda loot_name=loot: self.show_desc(loot_name)
            self.loot_frame.append(frame)
            self.loot_button.append(button)

    def draw_speed_up_button(self):
        button = Button(
            model="quad",
            text=">",
            scale=(0.1, 0.1),
            position=(0.8, 0.4),
            color=color.white,
            text_color=color.black,
        )
        button.on_click = lambda: self.speed_up()
        self.speed_button = button

    def speed_up(self):
        self.game.speed = self.game.speed + 0.5 if self.game.speed < 2 else 1
        self.speed_button.text = (
            ">>" if self.game.speed == 1.5 else ">>>" if self.game.speed == 2 else ">"
        )

    def draw_player_button(self):
        for i, name in enumerate(self.game.Character_Name):
            button = Button(
                model="quad",
                scale=(0.1, 0.1),
                position=(0.8 - (0.1 * i), -0.4),
                texture=f"assets/picture/Characters/{name}.png",
                color=color.white,
            )
            button.on_click = (
                lambda char_name=name: self.game.player_manager.character_spawn(
                    char_name
                )
            )
            button.alpha = 0.5
            button.parent = camera.ui
            self.game.buttons.append(button)

    def animate_indicator(self, level, wave):
        self.game.indicator_time += time.dt * self.game.speed
        if self.game.indicator_list:
            if self.game.indicator_time > 0.05:
                for path in self.game.indicator_list[:]:
                    if path:
                        entity_1, entity_2 = path.pop(0)
                        entity_1.animate_color(color.rgba(1, 0, 0), duration=0.3)
                        entity_2.animate_color(color.rgba(1, 0.6, 0.6), duration=0.3)
                        destroy(entity_1, 0.45 / self.game.speed)
                        destroy(entity_2, 0.45 / self.game.speed)
                        self.game.indicator_time = 0

    def show_indicator(self, level, wave):
        datas = self.game.data_manager.open_file(
            "Episodes", self.game.current_episode, f"Level {level}", "waves"
        )
        wave_data = datas[wave - 1]
        for data in wave_data["spawns"]:
            path_list = []
            gates = data["gates"]
            ai = self.game.enemy_manager.enemy_ai(gates - 1)
            path = ai[2]
            for i in range(len(path) - 1):
                x1, z1 = path[i]
                x2, z2 = path[i + 1]
                mid_x = (x1 + x2) / 2
                mid_z = (z1 + z2) / 2
                dx = x2 - x1
                dz = z2 - z1
                length = max(abs(dx), abs(dz)) or 0.001
                entity_1 = Entity(
                    model="cube",
                    color=color.rgba(0, 0, 0, 0),
                    position=(mid_x, 0.05, mid_z),
                    scale=(0.1 if dz else length, 0.02, 0.1 if dx else length),
                )
                entity_2 = Entity(
                    model="cube",
                    color=color.rgba(0, 0, 0, 0),
                    position=(mid_x, 0.05, mid_z),
                    scale=(
                        0.15 if dz else length * 1.2,
                        0.02 * 1.2,
                        0.15 if dx else length * 1.2,
                    ),
                )
                path_list.append([entity_1, entity_2])
            self.game.indicator_list.append(path_list)
        self.game.pathing = True

    def update_hp_bar(self, entity):
        entity.hp_bar.scale_x = max(0, entity.hp) / max(1, entity.max_hp)
        entity.hp_bar.color = (
            color.green
            if entity.hp / entity.max_hp > 0.7
            else (color.yellow if entity.hp / entity.max_hp > 0.3 else color.red)
        )


class Player(Entity):
    def __init__(
        self,
        attack_range,
        direction="Front",
        hp=100,
        damage=10,
        block_limit=1,
        layer=0,
        cooldown=1,
        can_block=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.attack_range = attack_range
        self.direction = direction
        self.hp = hp
        self.layer = layer
        self.damage = damage
        self.blocking = 0
        self.block_limit = block_limit
        self.max_hp = hp
        self.timer = 0
        self.cooldown = cooldown
        self.can_attack = False
        self.already_attack = False
        self.can_block = can_block


class Enemy(Entity):
    def __init__(
        self,
        attack_range,
        direction="Front",
        hp=100,
        damage=10,
        layer=0,
        cooldown=1,
        can_attack_units_on_high_ground=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.attack_range = attack_range
        self.direction = direction
        self.hp = hp
        self.layer = layer
        self.damage = damage
        self.max_hp = hp
        self.blocked = False
        self.cooldown = cooldown
        self.timer = 0
        self.can_attack = False
        self.blocking_player = None
        self.already_attack = False
        self.can_attack_units_on_high_ground = can_attack_units_on_high_ground
