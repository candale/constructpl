from os import path


with open(path.join(path.dirname(__file__), 'VERSION'), 'r') as ver_file:
    __version__ = ver_file.read().strip()
