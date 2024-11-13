import requests
import re
import json
import os
from menu import menu
from bs4 import BeautifulSoup
from selenium import webdriver


url = "https://animefire.plus/pesquisar/" + "-".join(input("Pesquisar anime: ").split())
# Your HTML content
html_content = requests.get(url)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content.text, 'html.parser')

# Find all the titles
titles_link = [div.article.a["href"] for div in soup.find_all('div', class_='col-6 col-sm-4 col-md-3 col-lg-2 mb-1 minWDanime divCardUltimosEps') if 'title' in div.attrs]
titles = [h3.get_text() for h3 in soup.find_all("h3", class_="animeTitle")]

selected = menu(titles)
if selected == "EXIT":
    exit()

url_episodes = titles_link[titles.index(selected)]

html_episodes_page = requests.get(url_episodes)
soup = BeautifulSoup(html_episodes_page.text, "html.parser")
episode_links = [a["href"] for a in soup.find_all('a', class_="lEp epT divNumEp smallbox px-2 mx-1 text-left d-flex")]
opts = [str(i) for i in range(1, len(episode_links)+1)]

selected = menu(opts)

if selected == "EXIT":
    exit()

url_episode = episode_links[int(selected) - 1]

season = 1
episode = selected
anime_slug = url_episode.split("/")[-2]

print(anime_slug)

res = requests.get("http://0.0.0.0:1010/episode/" + anime_slug + "/" + str(season) + "/" + episode)
json_res = json.loads(res.text)

for data in json_res["data"]:
    for episode in data["episodes"]:
        episode_link = episode["episode"]
        if episode_link is None:
            continue
        print(episode_link)
        if episode_link.startswith("https://www.blogger.com"):
            os.system(f"yt-dlp '{episode_link}' -o ./test.mp4 | vlc test.mp4.part --play-and-pause")
            os.system("rm ./test.mp4 ./test.mp4.part")
            break
        elif episode_link.endswith(".mp4"):
            os.system(f"vlc {episode_link} --play-and-pause") 
            break
