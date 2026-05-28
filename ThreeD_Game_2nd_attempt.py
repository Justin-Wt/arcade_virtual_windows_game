# Time: 21 hrs
from ursina import *
from collections import deque

app = Ursina()
tiles = []
players = []
buttons = []
spawning = False
spawned_player = None
hovered_tile = None
rotating = False
showing_range = False
key_pressed = ""


def rotation(attack_range):
    return [list(row) for row in zip(*attack_range[::-1])]


wave = 3, 5, 2, 1


def show_range(player):
    if player.direction == "Front":
        attack_range = rotation(rotation(player.attack_range))
    elif player.direction == "Left":
        attack_range = rotation(player.attack_range)
    elif player.direction == "Right":
        attack_range = rotation(rotation(rotation(player.attack_range)))
    elif player.direction == "Back":
        attack_range = player.attack_range

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
                        cube.world_position.x < player.position[0] + x + 0.5
                        and cube.world_position.x > player.position[0] + x - 0.5
                    ):
                        if (
                            cube.world_position.z < player.position[2] + z + 0.5
                            and cube.world_position.z > player.position[2] + z - 0.5
                        ):
                            cube.color = color.red


def spawn(i):
    global spawning, spawned_player
    spawning = True
    spawned_player = Entity(
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
        position=(mouse.world_point.x, 0.5, mouse.world_point.z),
    )


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


def input(key):
    global spawning, hovered_tile, rotating, showing_range, spawned_player, key_pressed
    if spawning and hovered_tile:
        if key == "left mouse down":
            print(hovered_tile.index)
            for player in players:
                if player.position == (
                    hovered_tile.position.x,
                    hovered_tile.index,
                    hovered_tile.position.z,
                ):
                    return
            spawned_player.position = (
                hovered_tile.x,
                hovered_tile.index,
                hovered_tile.z,
            )
            spawning = False
            rotating = True
            showing_range = True
    if rotating:
        if key == key_pressed:
            print("same key")
            key_pressed = ""
            showing_range = False
            players.append(spawned_player)
            rotating = False

        if key == "w":
            spawned_player.setH(0)
            spawned_player.direction = "Front"
            key_pressed = "w"

        if key == "s":
            spawned_player.setH(180)
            spawned_player.direction = "Back"
            key_pressed = "s"

        if key == "d":
            spawned_player.setH(90)
            spawned_player.direction = "Right"
            key_pressed = "d"

        if key == "a":
            spawned_player.setH(-90)
            spawned_player.direction = "Left"
            key_pressed = "a"


def update():
    global spawning, hovered_tile
    if enemy_1.path:
        next_position = enemy_1.path[0]
        speed = 1 * time.dt
        target = Vec3(next_position[0], 0.5, next_position[1])
        enemy_1.position += (target - enemy_1.position).normalized() * speed
        if distance(enemy_1.position, target) < 0.05:
            enemy_1.position = target
            enemy_1.path.pop(0)
    if not mouse.world_point:
        return
    for cube in tiles:
        if (
            mouse.world_point.x < cube.x + 0.5
            and mouse.world_point.x > cube.x - 0.5
            and mouse.world_point.z < cube.z + 0.5
            and mouse.world_point.z > cube.z - 0.5
        ):
            hovered_tile = cube
            hovered_tile.color = color.red
        else:
            if cube.index == 3:
                cube.color = color.blue
            elif cube.index == 2:
                cube.color = color.red
            else:
                cube.color = color.gray
    if spawning:
        spawned_player.position = (mouse.world_point.x, 0.5, mouse.world_point.z)
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
                    show_range(player)
                else:
                    player.color = color.white
            else:
                player.color = color.white
    if showing_range:
        show_range(spawned_player)
    speed = 5 * time.dt


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

enemy_1_asset = enemy_ai(0)
enemy_1 = Entity(
    model="cube",
    scale=(1, 1, 1),
    position=(enemy_1_asset[0][0], 0.5, enemy_1_asset[0][1]),
    texture="white_cube",
    color=color.black,
    collider="box",
    goal=enemy_1_asset[1],
    path=enemy_1_asset[2],
)
for i in range(1, 13):
    button = Button(
        model="quad",
        scale=(0.1, 0.1),
        position=(0.9 - (0.1 * i), -0.4),
        texture="assets/picture/Mona.png",
        color=color.white,
    )
    button.on_click = lambda i=i: spawn(i)
    button.alpha = 0.5
    button.parent = camera.ui
    buttons.append(button)

EditorCamera()

app.run()
