# MADED In 02 May 2026-04 May 2026
# Time: 1hr
import webview
import random
import json
import os

SAVE_FILE = "skill.json"


def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}


def load_stat(self):
    return {
        "strength": self.structure.strength,
        "hp": self.structure.hp,
        "defense": self.structure.defense,
        "SP": self.structure.SP,
    }


class Structure:
    def __init__(self):
        data = load_data()
        self.strength = data.get("strength", 0)
        self.hp = data.get("hp", 0)
        self.defense = data.get("defense", 0)
        self.SP = data.get("SP", 0)
        self.program = Program(self)


class Program:
    def __init__(self, structure):
        self.structure = structure

    def increase_stat(self, stat):
        if self.structure.SP <= 0:
            return getattr(self.structure, stat)
        current = getattr(self.structure, stat)
        self.structure.SP -= 1
        setattr(self.structure, stat, current + 1)
        data = {
            "strength": self.structure.strength,
            "hp": self.structure.hp,
            "defense": self.structure.defense,
            "SP": self.structure.SP,
        }
        save_data(data)
        return getattr(self.structure, stat)

    def decrease_stat(self, stat):
        self.structure.SP += 1
        current = getattr(self.structure, stat)
        setattr(self.structure, stat, current - 1)
        data = {
            "strength": self.structure.strength,
            "hp": self.structure.hp,
            "defense": self.structure.defense,
            "SP": self.structure.SP,
        }
        save_data(data)
        return getattr(self.structure, stat)


class API:
    def __init__(self, structure):
        self.structure = structure

    def load_stat(self):
        data = load_data()
        return {
            "strength": data.get("strength", 0),
            "hp": data.get("hp", 0),
            "defense": data.get("defense", 0),
            "SP": data.get("SP", 0),
        }

    def upgrade_stat(self, stat):
        self.structure.program.increase_stat(stat)
        return self.load_stat()

    def decrease_stat(self, stat):
        current = getattr(self.structure, stat)
        if current > 0:
            self.structure.program.decrease_stat(stat)
            return self.load_stat()
        else:
            return self.load_stat()


def open_window():
    screen_w, screen_h = webview.screens[0].width, webview.screens[0].height

    x = int(random.random() * (screen_w - 300))
    y = int(random.random() * (screen_h - 250))
    structure = Structure()
    api = API(structure)
    window = webview.create_window(
        "Skill",
        "skill.html",
        width=600,
        height=400,
        frameless=True,
        on_top=True,
        x=x,
        y=y,
        js_api=api,
    )

    webview.start()


if __name__ == "__main__":
    open_window()
