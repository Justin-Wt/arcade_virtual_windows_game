import arcade

speed = 5
update_frame = 40

right = 0
left = 1


def load_texture_pair(filename):
    return arcade.load_texture(filename)


class PlayerChar(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.char_face_dir = right

        self.cur_texture = 0

        self.scale = 1

        # adjust the collision box
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # load textures
        main_path = "assets/Demon/"

        # load textures for idle
        self.idle_texture = load_texture_pair(f"{main_path}Front_1.png")
        self.walk_texture = []
        for i in range(1, 3):
            self.texture = load_texture_pair(f"{main_path}Walk_{i}.png")
            self.walk_texture.append(self.texture)
        self.Back_texture = []
        for i in range(1, 3):
            self.texture = load_texture_pair(f"{main_path}Back_{i}.png")
            self.Back_texture.append(self.texture)
        self.Move_Forward = []
        for i in range(1, 3):
            self.texture = load_texture_pair(f"{main_path}Front_{i}.png")
            self.Move_Forward.append(self.texture)

    def update_animation(self, dir, delta_time=1 / 60):
        # L or R
        if self.change_x < 0 and self.char_face_dir == right:
            self.char_face_dir = left
        elif self.change_x > 0 and self.char_face_dir == left:
            self.char_face_dir = right

        # idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture
            return

        self.cur_texture += 1
        if self.cur_texture >= 2 * update_frame:
            self.cur_texture = 0
        frame = self.cur_texture // update_frame
        if dir == "Back":
            self.texture = self.Back_texture[frame]
        elif dir == "Front":
            self.texture = self.Move_Forward[frame]
        elif dir == "Left":
            self.texture = self.walk_texture[frame]
            self.scale_x = abs(self.scale_x)
        elif dir == "Right":
            self.texture = self.walk_texture[frame]
            self.scale_x = -abs(self.scale_x)
        else:
            self.texture = self.idle_texture
