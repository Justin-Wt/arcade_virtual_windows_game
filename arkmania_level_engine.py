# Time_In: {
#   Blender: "17 Hrs"
#   Python : "25 Hrs"
#   Tiled: "2 hrs:
# }

from ursina import *
from collections import deque
import json
from direct.actor.Actor import Actor


class Game:
    def __init__(self, filename):
        self.buttons = []
        self.models_type = ["Mona", "Moon"]
        self.grid, self.tiles = self.tile_maker(0)
        self.end_ui = []
        self.indicator_list = []
        self.pathing = False
        self.indicator_time = 0
        self.current_base_hp = 10
        self.base_hp = 10
        self.global_timer = 0
        self.hovered_tile = None
        self.rotating = False
        self.showing_range = False
        self.dragging = False
        self.end = False

        self.input_entity = Entity()
        self.update_entity = Entity()
        self.player_manager = PlayerManager(self)
        self.enemy_manager = EnemyManager(self)
        self.wave_manager = WaveManager(self)
        self.data_manager = Data_Manager(filename)
        self.ui_manager = UIManager(self)
        self.setup_ui()
        self.input_entity.input = self.input
        self.update_entity.update = self.update

    def setup_ui(self):
        self.ui_manager.create_hp_text(self.current_base_hp, self.base_hp)
        self.ui_manager.draw_player_button()
        self.ui_manager.draw_restart_button()

    def tile_maker(self, level):
        grid = [
            [2, 0, 1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
            [2, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 3],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [2, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
            [2, 0, 1, 1, 1, 0, 0, 1, 1, 1],
        ]
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

    def rotation(self, attack_range):
        return [list(row) for row in zip(*attack_range[::-1])]

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
            else:
                if cube.index == 3:
                    cube.color = color.rgba(0, 0, 0.8, 0.85)
                elif cube.index == 2:
                    cube.color = color.rgba(0.8, 0, 0, 0.85)
                else:
                    cube.color = color.gray

    def input(self, key):
        if key == "left mouse up" and self.dragging:
            if (
                self.player_manager.character_spawned_player
                not in self.player_manager.players
            ):
                self.player_manager.players.append(
                    self.player_manager.character_spawned_player
                )
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
        self.global_timer += time.dt
        print(window.size)
        self.enemy_manager.update()

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


class Data_Manager:
    def __init__(self, path):
        self.filepath = path

    def open_file(self, *keys):
        with open(self.filepath, "r") as f:
            data = json.load(f)

        current = data
        for key in keys:
            current = current[key]

        return current


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
        self.checking_enemy_spawn(level=1)
        if self.spawning_enemies:
            self.spawning_timer += time.dt
            self.update_spawn()
        if self.enemies:
            self.checking_paths()
            self.update_attack()

    def update_attack(self):
        for enemy in self.enemies:
            enemy.timer -= time.dt
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
        wave_time = []
        data = self.game.data_manager.open_file("Levels", f"Level {level}")
        for wave in data:
            timer, att = data[wave].items()
            _, times = timer
            wave_time.append(times)
        if self.game.wave_manager.wave_count < len(wave_time):
            if (
                self.game.global_timer
                > wave_time[self.game.wave_manager.wave_count] - 1
            ):
                if self.game.pathing == False:
                    self.game.ui_manager.show_indicator(
                        level, self.game.wave_manager.wave_count + 1
                    )
                else:
                    self.game.ui_manager.animate_indicator(
                        level, self.game.wave_manager.wave_count + 1
                    )
            if self.game.global_timer > wave_time[self.game.wave_manager.wave_count]:
                self.game.wave_manager.enemy_spawn_per_waves(
                    level, self.game.wave_manager.wave_count + 1
                )
                self.game.pathing = False
                self.game.wave_manager.wave_count += 1
        if self.game.wave_manager.wave_count == len(wave_time):
            if (
                not self.enemies
                and not self.spawning_enemies
                and self.game.current_base_hp > 0
                and not self.game.end
            ):
                self.game.ui_manager.end_screen("You Win")

    def checking_paths(self):
        for enemy in self.enemies:
            if enemy.path:
                next_position = enemy.path[0]
                for player in self.game.player_manager.players:
                    if (
                        next_position == (player.position.x, player.position.z)
                        and player.blocking < player.block_limit
                        and enemy.blocked == False
                    ):
                        player.blocking += 1
                        enemy.blocked = True
                        enemy.blocking_player = player
                    elif enemy.blocked:
                        break
                if enemy.blocked == False:
                    speed = 1 * time.dt
                    target = Vec3(next_position[0], 0.5, next_position[1])
                    dir_x = next_position[0] - enemy.position.x
                    dir_z = next_position[1] - enemy.position.z
                    if abs(dir_x) > abs(dir_z):
                        enemy.direction = "Back" if dir_x > 0 else "Front"
                    else:
                        enemy.direction = "Left" if dir_z > 0 else "Right"
                    enemy.position += (target - enemy.position).normalized() * speed
                    if distance(enemy.position, target) < 0.05:
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
                        player.color = color.red
                        self.show_range(player)
                    else:
                        player.color = color.white
                else:
                    player.color = color.white
                self.game.ui_manager.update_hp_bar(player)
                player.timer -= time.dt
                if player.timer <= 0:
                    player.can_attack = True
                if player.already_attack:
                    player.timer = player.cooldown
                    player.already_attack = False

    def update_spawn_range(self):
        if self.game.showing_range:
            self.show_range(self.character_spawned_player)

    def character_spawn(self, i):
        data = self.game.data_manager.open_file("Models", self.game.models_type[i - 1])
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
            "Levels", f"Level {level}", f"wave {wave}", "spawns"
        )
        for data in datas:
            e_type, amounts, gates = data.values()
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

    def draw_restart_button(self):
        restart_button = Button(
            model="quad", scale=(0.1, 0.1), position=(-0.9, 0.5), color=color.red
        )
        restart_button.on_click = self.game.restarting

    def draw_player_button(self):
        for i in range(1, 3):
            button = Button(
                model="quad",
                scale=(0.1, 0.1),
                position=(0.9 - (0.1 * i), -0.4),
                texture="assets/picture/Mona.png",
                color=color.white,
            )
            button.on_click = lambda i=i: self.game.player_manager.character_spawn(i)
            button.alpha = 0.5
            button.parent = camera.ui
            self.game.buttons.append(button)

    def animate_indicator(self, level, wave):
        self.game.indicator_time += time.dt
        if self.game.indicator_list:
            if self.game.indicator_time > 0.05:
                for path in self.game.indicator_list[:]:
                    if path:
                        entity_1, entity_2 = path.pop(0)
                        entity_1.animate_color(color.rgba(1, 0, 0), duration=0.3)
                        entity_2.animate_color(color.rgba(1, 0.6, 0.6), duration=0.3)
                        destroy(entity_1, 0.45)
                        destroy(entity_2, 0.45)
                        self.game.indicator_time = 0

    def show_indicator(self, level, wave):
        datas = self.game.data_manager.open_file(
            "Levels", f"Level {level}", f"wave {wave}", "spawns"
        )
        for data in datas:
            path_list = []
            _, _, gates = data.values()
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
        entity.hp_bar.scale_x = entity.hp / entity.max_hp
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


class Enemy(Entity):
    def __init__(
        self,
        attack_range,
        direction="Front",
        hp=100,
        damage=10,
        layer=0,
        cooldown=1,
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
