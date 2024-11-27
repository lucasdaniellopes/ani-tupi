import loader
from menu import menu
from repository import rep
from loader import PluginInterface

if __name__=="__main__":
    loader.load_plugins(["animefire"], {"pt-br"})
    
    query = input("Pesquise anime: ")
    for source in rep.get_sources():
        source.search_anime(query)
