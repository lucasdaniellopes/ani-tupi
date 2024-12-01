import importlib


class PluginInterface:
    pass

def load_plugins(plugins: list[str], languages_dict: list) -> None:
    for plugin in plugins:
        plugin = importlib.import_module("plugins." + plugin)
        plugin.load(languages_dict)

