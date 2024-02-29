import os


with open(os.path.join(os.path.dirname(__file__), 'VERSION'), encoding="utf-8") as f:
    VERSION = f.read().strip()
