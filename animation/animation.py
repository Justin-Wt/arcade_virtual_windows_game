import tkinter as tk
from frame_maker import animate
root = tk.Tk()
root.attributes("-topmost", True)
root.attributes("-fullscreen", True)
root.attributes("-transparentcolor", "black")
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)
chisa=animate("animation_frames/chisa/frame_",49,0.5,30,200,740,canvas)
march_7th=animate("animation_frames/march 7th/frame_",10,0.5,70,1400,760,canvas)

chisa.update()
march_7th.update()
root.mainloop()