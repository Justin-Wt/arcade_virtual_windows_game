# fmt:off
from ursina import*;from arkmania_main_menu_engine import main_menu;app=Ursina(title="Arkmania",icon="assets/icons/Arkmania_Icon.ico",development_mode=False);window.borderless = False;window.fullscreen = False;window.size = (1280, 720);main_menu("assets/tile/main_menu.tmj");EditorCamera();app.run()
