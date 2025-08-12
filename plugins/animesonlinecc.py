import requests
import subprocess
from bs4 import BeautifulSoup
from repository import rep
from loader import PluginInterface
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing.pool import ThreadPool
from os import cpu_count
from .utils import is_firefox_installed_as_snap


class AnimesOnlineCC(PluginInterface):
    languages = ["pt-br"]
    name = "animesonlinecc"
    quality = 480
    
    @staticmethod
    def search_anime(query):
        url = "https://animesonlinecc.to/search/" + "+".join(query.split())
        html_content = requests.get(url)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        divs = soup.find_all('div', class_='data')
        titles_urls = [div.h3.a["href"] for div in divs]
        titles = [div.h3.a.get_text() for div in divs]
        for title, url in zip(titles, titles_urls):
            rep.add_anime(title, url, AnimesOnlineCC.name)

        def parse_seasons(title, url):
                html = requests.get(url)
                soup = BeautifulSoup(html.text, 'html.parser')
                num_seasons = len([div for div in soup.find_all('div', class_='se-c')])
                if num_seasons > 1:
                    for n in range(2, num_seasons + 1):
                        rep.add_anime(title + " Season " + str(n), url, AnimesOnlineCC.name, n)
        
        with ThreadPool(cpu_count()) as pool:
            for title, url in zip(titles, titles_urls):
                pool.apply(parse_seasons, args=(title, url))
            
    @staticmethod
    def search_episodes(anime, url, season):
        html_episodes_page = requests.get(url)
        soup = BeautifulSoup(html_episodes_page.text, "html.parser")
        seasons = [ season for season in soup.find_all('ul', class_="episodios") ]
        season = seasons[ season - 1 if season is not None else 0]
        urls, titles = [], []
        for div in season.find_all('div', class_="episodiotitle"):
            urls.append(div.a["href"])
            titles.append(div.a.get_text()) 
        rep.add_episode_list(anime, titles, urls, AnimesOnlineCC.name)
    
    @staticmethod
    def search_player_src(url_episode, container, event):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        try:
            if is_firefox_installed_as_snap():
                service = webdriver.FirefoxService(executable_path="/snap/bin/geckodriver")
                driver = webdriver.Firefox(options=options, service = service)
            else:
                driver = webdriver.Firefox(options=options)
        except:
            raise Exception("Firefox not installed.")

        driver.get(url_episode)

        try:
            class_ = "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/iframe"
            params = (By.XPATH, class_)
            element = WebDriverWait(driver, 7).until(
                EC.visibility_of_all_elements_located(params)
            )
        except:
            driver.quit()
            raise Exception("nor iframe nor video tags were found in animesonlinecc.")

        product = driver.find_element(params[0], params[1])
        link = product.get_property("src")
        
        if "/sd/" in link:
            link = link.replace("/sd/", "/hd/")
        driver.quit()

        if not event.is_set():
            container.append(link)
            event.set()


def load(languages_dict):
    can_load = False
    for language in AnimesOnlineCC.languages:
        if language in languages_dict:
            can_load = True
            break
    if not can_load:
        return
    rep.register(AnimesOnlineCC)