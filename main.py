import requests
import json
import os
from menu import menu
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__=="__main__":
    url = "https://animefire.plus/pesquisar/" + "-".join(input("Pesquisar anime: ").split())
    print("Buscando...")
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
    print("Carregando video encontrado em:", url_episode)
    # instantiate a Chrome options object
    options =webdriver.ChromeOptions()
    # set the options to use Chrome in headless mode
    options.add_argument("--headless=new")
    # initialize an instance of the Chrome driver (browser) in headless mode
    driver = webdriver.Chrome(options=options)
    # visit your target site
    driver.get(url_episode)

    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.ID, "my-video_html5_api"))
        )
    except:
        print("AnimeFire não tem mais esse video ou foi hospedado no YouTube.")
        exit()

    product = driver.find_element(By.ID, "my-video_html5_api")

    link = product.get_property("src")
    os.system(f"mpv '{link}'")
