# Time: 18 hrs
from ursina import *
from collections import deque

app = Ursina()
tiles = []
players = []


def rotation(attack_range):
    return [list(row) for row in zip(*attack_range[::-1])]


def show_range(attack_range, position):
    if player.direction == "Front":
        attack_range = rotation(rotation(attack_range))
    elif player.direction == "Left":
        attack_range = rotation(attack_range)
    elif player.direction == "Right":
        attack_range = rotation(rotation(rotation(attack_range)))

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
                for cube in tiles:
                    if (
                        cube.world_position.x < position[0] + x + 0.5
                        and cube.world_position.x > position[0] + x - 0.5
                    ):
                        if (
                            cube.world_position.z < position[2] + z + 0.5
                            and cube.world_position.z > position[2] + z - 0.5
                        ):
                            cube.color = color.red


def enemy_ai(enemy=0):
    starts = []
    for cube in tiles:
        if cube.index == 3:
            goal = (cube.world_position.x, cube.world_position.z)
        elif cube.index == 2:
            starts.append((cube.world_position.x, cube.world_position.z))
    queue = deque([(starts[enemy], [])])
    visited = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while queue:
        (x, z), path = queue.popleft()
        if (x, z) in visited:
            continue
        visited.add((x, z))
        path = path + [(x, z)]
        if (x, z) == goal:
            return starts[enemy], goal, path
        for dx, dz in directions:
            nx = x + dx
            nz = z + dz
            if 0 <= nx < len(grid[0]) and 0 <= nz < len(grid):
                if grid[int(nz)][int(nx)] != 1:
                    queue.append(((nx, nz), path))


def update():
    if not mouse.world_point:
        return
    if enemy_1.path:
        next_position = enemy_1.path[0]
        speed = 1 * time.dt
        if enemy_1.x < next_position[0]:
            enemy_1.x += min(speed, next_position[0] - enemy_1.x)
        elif enemy_1.x > next_position[0]:
            enemy_1.x -= min(speed, enemy_1.x - next_position[0])
        if enemy_1.z < next_position[1]:
            enemy_1.z += min(speed, next_position[1] - enemy_1.z)
        elif enemy_1.z > next_position[1]:
            enemy_1.z -= min(speed, enemy_1.z - next_position[1])
        if (
            abs(enemy_1.x - next_position[0]) < 0.01
            and abs(enemy_1.z - next_position[1]) < 0.01
        ):
            enemy_1.position = (next_position[0], 0.5, next_position[1])
            enemy_1.path.pop(0)
    for cube in tiles:
        if (
            mouse.world_point.x < cube.world_position.x + 0.5
            and mouse.world_point.x > cube.world_position.x - 0.5
        ):
            if (
                mouse.world_point.z < cube.world_position.z + 0.5
                and mouse.world_point.z > cube.world_position.z - 0.5
            ):
                cube.color = color.red
            else:
                if cube.index == 3:
                    cube.color = color.blue
                elif cube.index == 2:
                    cube.color = color.red
                else:
                    cube.color = color.gray
        else:
            if cube.index == 3:
                cube.color = color.blue
            elif cube.index == 2:
                cube.color = color.red
            else:
                cube.color = color.gray
    if players:
        for player in players:
            if (
                mouse.world_point.x < player.world_position.x + 0.5
                and mouse.world_point.x > player.world_position.x - 0.5
            ):
                if (
                    mouse.world_point.z < player.world_position.z + 0.5
                    and mouse.world_point.z > player.world_position.z - 0.5
                ):
                    player.color = color.red
                    show_range(player.attack_range, player.position)
                else:
                    player.color = color.white
            else:
                player.color = color.white
    speed = 5 * time.dt
    if held_keys["w"]:
        player.setH(0)
        player.direction = "Front"

    if held_keys["s"]:
        player.setH(180)
        player.direction = "Back"

    if held_keys["d"]:
        player.setH(90)
        player.direction = "Right"

    if held_keys["a"]:
        player.setH(-90)
        player.direction = "Left"


grid = [
    [2, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [2, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]
player_position = [5, 0, 5]
for x in range(len(grid)):
    for z in range(len(grid[0])):
        height = 1 if grid[z][x] > 0 else 0
        tile = Entity(
            model="cube",
            scale=(1, 0.1 + height, 1),
            position=(x, height / 2, z),
            texture="white_cube",
            index=grid[z][x],
            color=(
                color.blue
                if grid[z][x] == 3
                else color.red if grid[z][x] == 2 else color.gray
            ),
            collider="box",
        )
        tiles.append(tile)
player = Entity(
    model="assets/3D Models/Mona.gltf",
    collider="box",
    attack_range=[
        [1, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
    ],
    direction="Front",
    type="Ranged",
)
player.reparentTo(render)
player.setPos(*player_position)
players.append(player)
main = "ValveBiped.Bip01_Pelvis|ValveBiped.Bip01_Pelvis|ValveBiped..0"
enemy_1_asset = enemy_ai(0)
enemy_1 = Entity(
    model="cube",
    scale=(1, 1, 1),
    position=enemy_1_asset[0] + (0, 0.5, 0),
    texture="white_cube",
    color=color.black,
    collider="box",
    goal=enemy_1_asset[1],
    path=enemy_1_asset[2],
)

EditorCamera()

app.run()
