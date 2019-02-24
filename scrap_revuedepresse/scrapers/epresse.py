import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_epresse(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features='lxml')
    url = soup.find_all('span', {'class': 'cover'})[1].find_all('img')[0]['src']
    urllib.request.urlretrieve(url, filename)
