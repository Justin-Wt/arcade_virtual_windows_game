import arcade
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class icon_maker:
    def __init__(self,width,height):
        self.icon=0
        self.width=width
        self.height=height
        self.bg=None
    def create_icon(self,image,texts):
        row=(self.icon%8)*100+50
        column=(self.icon//8)*100+50
        x = column
        y = self.height - row - 12.5
        rect=x,y,50,50
        texture=arcade.load_texture(os.path.join(BASE_DIR, "assets","UI's",f"{image}.png"))
        text=arcade.Text(texts,column-(len(texts)*4),y-37.5,arcade.color.WHITE,font_size=14)
        self.icon+=1
        return {
            "rect":rect,
            "texture":texture,
            "text":text
        }

    