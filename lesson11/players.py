import arcade

speed=5
update_frame=5

right=0
left=1
def load_texture_pair(filename):
    return arcade.load_texture(filename)

class PlayerChar(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.char_face_dir=right

        self.cur_texture=0

        self.scale=0.8

        #adjust the collision box
        self.points=[[-22,-64],[22,-64],[22,28],[-22,28]]

        #load textures
        main_path=":resources:images/animated_characters/robot/robot"

        #load textures for idle
        self.idle_texture=load_texture_pair(f"{main_path}_idle.png")
        self.walk_texture=[]
        for i in range(8):
            self.texture=load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_texture.append(self.texture)

    def update_animation(self, delta_time = 1 / 60):
        #L or R
        if self.change_x<0 and self.char_face_dir==right:
            self.char_face_dir=left
        elif self.change_x>0 and self.char_face_dir==left:
            self.char_face_dir=right
        
        #set scale X based on dir(negative scale flips)
        self.scale_x = abs(self.scale_x) if self.char_face_dir == right else -abs(self.scale_x) #ternery operator using if else in 1 line

        #idle animation
        if self.change_x==0 and self.change_y==0:
            self.texture=self.idle_texture
            return

        self.cur_texture+=1
        if self.cur_texture>7 * update_frame:
            self.cur_texture=0
        frame=self.cur_texture//update_frame
        self.texture=self.walk_texture[frame]