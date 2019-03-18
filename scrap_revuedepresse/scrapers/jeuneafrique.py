import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_jeuneafrique(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features='lxml')
    url = soup.find_all('img', {'class': 'ui image'})[0]['src']
    url = f"https:{url}"
    urllib.request.urlretrieve(url, filename)
