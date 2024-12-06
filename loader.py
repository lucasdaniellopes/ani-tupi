import importlib
from abc import ABC, abstractstaticmethod
from os.path import isfile, join
from os import listdir


class PluginInterface(ABC):

    @abstractstaticmethod
    def search_anime():
        raise NotImplementedError

    @abstractstaticmethod
    def search_episodes():
        raise NotImplementedError

    @abstractstaticmethod
    def search_player_src():
        raise NotImplementedError


def load_plugins(languages: dict, plugins = None) -> None:
    path = "plugins/"
    system = {"__init__.py", "utils.py"}
    plugins = plugins if plugins is not None else [file[:-3] for file in listdir(path) if isfile(join(path, file)) and file not in system] 
    for plugin in plugins:
        plugin = importlib.import_module("plugins." + plugin)
        plugin.load(languages)

