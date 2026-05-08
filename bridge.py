import subprocess
import sys


def open_window(path):
    subprocess.Popen([sys.executable, f"{path}.py"])
