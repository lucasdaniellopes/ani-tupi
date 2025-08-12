import requests
from bs4 import BeautifulSoup
from repository import rep
from loader import PluginInterface
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import is_firefox_installed_as_snap
import re
import json
import urllib.parse


class AnimeDrive(PluginInterface):
    languages = ["pt-br"]
    name = "animedrive"
    quality = 1080
    
    @staticmethod
    def search_anime(query):
        url = f"https://animesdrive.blog/?s={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            html_content = requests.get(url, headers=headers)
            soup = BeautifulSoup(html_content.text, 'html.parser')
            
            results = soup.find_all('div', class_='result-item')
            
            for result in results:
                details = result.find('div', class_='details')
                if details:
                    title_div = details.find('div', class_='title')
                    if title_div and title_div.find('a'):
                        link = title_div.find('a')
                        anime_url = link.get('href')
                        title = link.get_text().strip()
                        
                        if title and anime_url:
                            rep.add_anime(title, anime_url, AnimeDrive.name)
                        
        except Exception as e:
            print(f"Erro ao buscar animes no AnimeDrive: {e}")
    
    @staticmethod
    def search_episodes(anime, url, params):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            html_episodes_page = requests.get(url, headers=headers)
            soup = BeautifulSoup(html_episodes_page.text, "html.parser")
            
            episode_list = []
            episode_links = []
            
            seasons_container = soup.find('div', id='seasons')
            if seasons_container:
                season_divs = seasons_container.find_all('div', class_='se-c')
                
                for season_div in season_divs:
                    episodes_ul = season_div.find('ul', class_='episodios')
                    if episodes_ul:
                        episodes_li = episodes_ul.find_all('li')
                        
                        for ep_li in episodes_li:
                            episode_title_div = ep_li.find('div', class_='episodiotitle')
                            if episode_title_div:
                                ep_link = episode_title_div.find('a', href=True)
                                if ep_link:
                                    href = ep_link.get('href')
                                    text = ep_link.get_text().strip()
                                    
                                    if not href.startswith('http'):
                                        href = f"https://animesdrive.blog{href}"
                                    
                                    episode_list.append(text)
                                    episode_links.append(href)
            
            if not episode_list:
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href')
                    text = link.get_text().strip()
                    
                    if href and '/episodio/' in href and 'Episódio' in text:
                        if not href.startswith('http'):
                            href = f"https://animesdrive.blog{href}"
                        
                        episode_list.append(text)
                        episode_links.append(href)
            
            if not episode_list:
                episode_list.append("Episódio Único")
                episode_links.append(url)
            
            rep.add_episode_list(anime, episode_list, episode_links, AnimeDrive.name)
            
        except Exception as e:
            print(f"Erro ao buscar episódios no AnimeDrive: {e}")
    
    @staticmethod
    def search_player_src(url_episode, container, event):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url_episode, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            player_options = soup.find_all('li', class_='dooplay_player_option')
            
            if not player_options:
                raise Exception("Nenhum player encontrado na página")
            
            all_links = []
            
            for i, player_option in enumerate(player_options):
                try:
                    post_id = player_option.get('data-post')
                    player_num = player_option.get('data-nume')
                    player_type = player_option.get('data-type')
                    
                    if not post_id or not player_num:
                        continue
                    
                    ajax_url = "https://animesdrive.blog/wp-admin/admin-ajax.php"
                    
                    ajax_headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Referer': url_episode
                    }
                    
                    data = {
                        'action': 'doo_player_ajax',
                        'post': post_id,
                        'nume': player_num,
                        'type': player_type if player_type else 'tv'
                    }
                    
                    ajax_response = requests.post(ajax_url, headers=ajax_headers, data=data)
                    
                    if ajax_response.status_code == 200:
                        json_data = json.loads(ajax_response.text)
                        
                        if 'embed_url' in json_data:
                            embed_url = json_data['embed_url']
                            
                            parsed = urllib.parse.urlparse(embed_url)
                            params = urllib.parse.parse_qs(parsed.query)
                            
                            if 'source' in params and params['source']:
                                mp4_url = urllib.parse.unquote(params['source'][0])
                                
                                if mp4_url.endswith('.mp4'):
                                    if 'eos.feralhosting.com' in mp4_url or 'animeflix.blog' in mp4_url:
                                        all_links.append(mp4_url)
                                    
                except Exception as e:
                    print(f"Erro ao tentar player {i+1}: {e}")
                    continue
            
            if all_links:
                chosen_link = None
                
                server_priority = ['eos.feralhosting.com', 'animeflix.blog']
                
                for server in server_priority:
                    server_links = [link for link in all_links if server in link]
                    
                    if server_links:
                        hd_links = [link for link in server_links if '/hd/' in link.lower() or 'hd' in link.lower()]
                        
                        if hd_links:
                            chosen_link = hd_links[0]
                            break
                        else:
                            sd_links = [link for link in server_links if '/sd/' in link]
                            
                            if sd_links:
                                chosen_link = sd_links[0].replace('/sd/', '/hd/')
                                break
                            elif server_links:
                                chosen_link = server_links[0]
                                break
                
                if not chosen_link and all_links:
                    chosen_link = all_links[0]
                
                if chosen_link and not event.is_set():
                    container.append(chosen_link)
                    event.set()
                    return
            
            raise Exception("Não foi possível extrair o link do vídeo de nenhum player")
                
        except Exception as e:
            print(f"Erro ao extrair player do AnimeDrive: {e}")
            raise e


def load(languages_dict):
    can_load = False
    for language in AnimeDrive.languages:
        if language in languages_dict:
            can_load = True
            break
    if not can_load:
        return
    rep.register(AnimeDrive)