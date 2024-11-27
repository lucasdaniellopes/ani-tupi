import loader
import threading
from menu import menu
from repository import rep
from loader import PluginInterface


if __name__=="__main__":
    loader.load_plugins(["animefire"], {"pt-br"})
    
    query = input("Pesquise anime: ")
    rep.search_anime(query)

    selected_anime = menu(rep.get_anime_titles())
    print(selected_anime)
    
    rep.search_episodes(selected_anime)
    selected_episode = menu(rep.get_anime_titles())

    print(selected_episode)
