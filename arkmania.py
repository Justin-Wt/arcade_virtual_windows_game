from ursina import *
from arkmania_level_engine import Game

app = Ursina()
game = Game("arkmania.json")
EditorCamera()
app.run()
