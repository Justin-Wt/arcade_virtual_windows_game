from PIL import Image, ImageTk
class animate:
    def __init__(self,path,frames,scale,speed,x,y,canvas):
        self.path=path
        self.frames=frames+1
        self.speed=speed
        self.x=x
        self.scale=scale
        self.y=y
        self.canvas=canvas
        self.frame_index=0
        self.frame=[]
        for i in range(1,self.frames):
            img=Image.open(f"animation/{self.path}{i:04d}-removebg-preview.png")
            new_size = (int(img.width * self.scale), int(img.height * self.scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            self.frame.append(ImageTk.PhotoImage(img))
        self.image_id=self.canvas.create_image(self.x, self.y, image=self.frame[0])
    def update(self):
        self.frame_index = (self.frame_index + 1) % len(self.frame)
        self.canvas.itemconfig(self.image_id, image=self.frame[self.frame_index])

        self.canvas.after(self.speed,self.update)