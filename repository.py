import asyncio
from os import cpu_count
from loader import PluginInterface
from typing import Callable
from collections import defaultdict
from threading import Thread, Condition
from concurrent.futures import ThreadPoolExecutor


class Repository:
    """ get for methods called by main that return some value
        search for methods called by main that don't return but affects state
        add for methods called by any plugin that affects state
        register should be called by a loader function """

    _instance = None
    
    def __init__(self) -> None:
        self.sources = []
        self.anime_to_urls = defaultdict(list)
        self.anime_episodes_titles = defaultdict(list)
        self.anime_episodes_urls = defaultdict(list)
    
    def __new__(cls):
        if not Repository._instance:
            Repository._instance = super(Repository, cls).__new__(cls)
        return Repository._instance

    def register(self, plugin: PluginInterface) -> None:
        self.sources.append(plugin)
    
    def search_anime(self, query: str) -> None:
        for source in rep.sources:
            source.search_anime(query)
    
    def add_anime(self, title: str, url: str, F: Callable[[str, str], None]) -> None:
        """
        This method assumes that different seasons are different anime, like MAL, so plugin devs should take scrape that way.
        TODO: create algorithm to consider the different anime titles for the same anime in each website as one. 
        """
        
        self.anime_to_urls[title].append((url, F))

    def get_anime_titles(self) -> list[str]:
        return list(self.anime_to_urls.keys())
    
    def search_episodes(self, anime: str) -> list[str]:
        if anime in self.anime_episodes_titles:
            return self.anime_episode_titles[anime]

        urls_and_scrapers = rep.anime_to_urls[anime]
        threads = [Thread(target=F, args=(anime, url,)) for url, F in urls_and_scrapers]
        
        for th in threads:
            th.start()

        for th in threads:
            th.join()
    
    def add_episode_list(self, anime: str, title_list: list[str], url_list: list[str], F: Callable[[...], None]) -> None:
        self.anime_episodes_titles[anime].append(title_list)
        self.anime_episodes_urls[anime].append((url_list, F))
    
    def get_episode_list(self, anime: str):
        return self.anime_episodes_titles[anime][0]

    def search_player(self, anime: str, episode_num: int) -> None:
        """
        This method assumes all episode lists to be the same size, plugin devs should guarantee that OVA's are not considered.
        """
        selected_urls = []
        for urls, F in self.anime_episodes_urls[anime]:
            selected_urls.append((urls[episode_num - 1], F))

        async def search_all_sources():
            nonlocal selected_urls, self
            event = asyncio.Event()
            container = []
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                tasks = [loop.run_in_executor(executor, F, url, container, event) for url, F in selected_urls]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED) 

                for task in pending:
                    task.cancel()
                return container[0]

        return asyncio.run(search_all_sources())
        
rep = Repository()

if __name__=="__main__":
    rep3, rep2 = Repository(), Repository()
    print(rep3 is rep2)
