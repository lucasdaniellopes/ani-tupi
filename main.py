import loader
import argparse
from menu import menu
from repository import rep
from loader import PluginInterface
from video_player import play_video


if __name__=="__main__":
    parser = argparse.ArgumentParser(
                prog = "ani-tupi",
                description="Veja anime sem sair do terminal."
            )
    parser.add_argument("--query", "-q")
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()

    loader.load_plugins(["animefire"], {"pt-br"})
    
    query = (input("Pesquise anime: ") if not args.query else args.query) if not args.debug else "eva"

    rep.search_anime(query)
    selected_anime = menu(rep.get_anime_titles(), msg="Escolha o Anime.")
    
    rep.search_episodes(selected_anime)
    episode_list = rep.get_episode_list(selected_anime)
    selected_episode = menu(episode_list, msg="Escolha o episódio.")
    episode_idx = episode_list.index(selected_episode) 
    while True:
        player_url = rep.search_player(selected_anime, episode_idx + 1)
        play_video(player_url, args.debug)

        opts = []
        print(episode_idx, len(episode_list) -1, episode_list)
        if episode_idx < len(episode_list) - 1:
            opts.append("Próximo")
        if episode_idx > 0:
            opts.append("Anterior")

        selected_opt = menu(opts, msg="O que quer fazer agora?")

        if selected_opt == "Próximo":
            episode_idx += 1 
        elif selected_opt == "Anterior":
            episode_idx -= 1



