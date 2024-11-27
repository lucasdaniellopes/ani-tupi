import requests
from bs4 import BeautifulSoup
from repository import rep
from loader import PluginInterface


class AnimeFire(PluginInterface):
    languages = ["pt-br"]
    name = "animefire"
    
    @staticmethod
    def get_anime(query):
        url = "https://animefire.plus/pesquisar/" + "-".join(query.split())
        html_content = requests.get(url)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        titles_urls = [div.article.a["href"] for div in soup.find_all('div', class_='col-6 col-sm-4 col-md-3 col-lg-2 mb-1 minWDanime divCardUltimosEps') if 'title' in div.attrs]
        titles = [h3.get_text() for h3 in soup.find_all("h3", class_="animeTitle")]

        for title, url in zip(titles, titles_urls):
            rep.add_anime(title, url, AnimeFire.get_episodes)
    
    @staticmethod
    def get_episodes(anime, url):
        html_episodes_page = requests.get(url)
        soup = BeautifulSoup(html_episodes_page.text, "html.parser")
        episode_links = [a["href"] for a in soup.find_all('a', class_="lEp epT divNumEp smallbox px-2 mx-1 text-left d-flex")]
        opts = [a.get_text() for a in soup.find_all('a', class_="lEp epT divNumEp smallbox px-2 mx-1 text-left d-flex")]

        rep.add_episode_list(anime, opts, episode_links, AnimeFire.get_player_src) 
    
    @staticmethod
    def get_player_src():
        pass


def load(languages_dict):
    can_load = False
    for language in AnimeFire.languages:
        if language in languages_dict:
            can_load = True
            break
    if not can_load:
        return
    rep.register(AnimeFire)
    

