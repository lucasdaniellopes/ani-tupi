import loader
import argparse
from menu import menu
from repository import rep
from loader import PluginInterface
from video_player import play_video
from json import load, dump


def history():
    with open("history.json", "r+") as f:
        data = load(f)
        titles = dict()
        for entry, info in data.items():
            ep_info = f" (Episódio {info[1]})"
            titles[entry + ep_info] = len(ep_info)
        selected = menu(list(titles.keys()), msg="Continue assistindo.")
        anime = selected[:-titles[selected]]
        episode = data[anime][1]
        rep.anime_episodes_urls[anime] = data[anime][0]
        del data[anime]
        dump(data, f)
    return anime, episode

def save_history(anime, episode):
    with open("history.json", "w+") as f:
        try:
            data = load(f)
        except:
            data = dict()

        data[anime] = [rep.anime_episodes_urls[anime],
                       episode]
        dump(data, f)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                prog = "ani-tupi",
                description="Veja anime sem sair do terminal."
            )
    parser.add_argument("--query", "-q")
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument("--continue_watching", "-c", action="store_true")
    args = parser.parse_args()

    loader.load_plugins({"pt-br"}, None if not args.debug else ["animesonlinecc"])
    
    if not args.continue_watching:
        query = (input("Pesquise anime: ") if not args.query else args.query) if not args.debug else "eva"
        rep.search_anime(query)
        titles = rep.get_anime_titles()
        selected_anime = menu(titles, msg="Escolha o Anime.")

        rep.search_episodes(selected_anime)
        episode_list = rep.get_episode_list(selected_anime)
        selected_episode = menu(episode_list, msg="Escolha o episódio.")

        episode_idx = episode_list.index(selected_episode) 
    else:
        selected_anime, episode_idx = history()
    
    num_episodes = len(rep.anime_episodes_urls[selected_anime][0][0])
    while True:
        episode = episode_idx + 1
        player_url = rep.search_player(selected_anime, episode)
        if args.debug: print(player_url)
        play_video(player_url, args.debug)
        save_history(selected_anime, episode)

        opts = []
        if episode_idx < num_episodes - 1:
            opts.append("Próximo")
        if episode_idx > 0:
            opts.append("Anterior")

        selected_opt = menu(opts, msg="O que quer fazer agora?")

        if selected_opt == "Próximo":
            episode_idx += 1 
        elif selected_opt == "Anterior":
            episode_idx -= 1
