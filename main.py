import repository
import loader
from menu import menu

if __name__=="__main__":
    loader.load_plugins(["animefire"], {"pt-br"})
    
    query = input("Pesquise anime: ")
    
    for source in repository.sources:
        source.search_anime(query)

    selected_title = menu(repository.anime_titles) 
    title_urls = repository.anime_titles_urls[repository.anime_titles.index(selected_title)]

    for source in repository.sources:
        source.get_episodes(title_urls)

    selected_episode = menu(repository.episode_titles, "Escolha o episódio")
    episode_url = repository.episode_urls[repository.episode_titles.index(selected_episode)]

    for source in repository.sources:
        source.find_player_source()

    repository.play_episode()
