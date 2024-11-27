from loader import PluginInterface
from typing import Callable
from collections import defaultdict
from threading import Thread


class Repository:
    """ get for methods called by main that return some value
        search for methods called by main that don't return but affects state
        add for methods called by any plugin that affects state
        register should be called by a loader function """

    instance = None
    
    def __init__(self) -> None:
        if Repository.instance:
            return Repository.instance
        Repository.instance = self
        self.sources = []
        self.anime_to_urls = defaultdict(list)
        self.anime_episodes_titles = defaultdict(list)
        self.anime_episodes_urls = defaultdict(list)

    def register(self, plugin: PluginInterface) -> None:
        self.sources.append(plugin)
    
    def add_anime(self, title: str, url: str, F: Callable[[str, str], None]) -> None:
        self.anime_to_urls[title].append((url, F))

    def get_anime_titles(self) -> list[str]:
        return list(self.anime_to_urls.keys())
    
    def search_anime(self, query: str) -> None:
        for source in rep.sources:
            source.search_anime(query)
    
    def search_episodes(self, anime: str) -> list[str]:
        if anime in self.anime_episodes_titles:
            return self.anime_episode_titles[anime]

        urls_and_scrapers = rep.anime_to_urls[anime]
        threads = [Thread(target=F, args=(anime, url,)) for url, F in urls_and_scrapers]
        
        for th in threads:
            th.start()

        for th in threads:
            th.join()
    
    def add_episode_list(self, anime: str, title_list: list[str], url_list: list[str], F: Callable[[str, str], None]) -> None:
        self.anime_episodes_titles[anime].append(title_list)
        self.anime_episodes_urls[anime].append((url_list, F))


        
rep = Repository()

