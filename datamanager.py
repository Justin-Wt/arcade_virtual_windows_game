import json


class Data_Manager:
    def __init__(self, path):
        self.filepath = path

    def open_file(self, *keys):
        with open(self.filepath, "r") as f:
            data = json.load(f)
        current = data
        for key in keys:
            current = current[key]
        return current
