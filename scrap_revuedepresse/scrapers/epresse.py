import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_epresse(url, filename, auj):
    try:
        url_auj = f"{url.rstrip('/')}/{auj}"
        html_doc = requests.get(url_auj).content
        soup = BeautifulSoup(html_doc, features='lxml')
        url_img = soup.find_all('span', {'class': 'cover'})[1].find_all('img')[0]['src']
        urllib.request.urlretrieve(url_img, filename)
    except:
        html_doc = requests.get(url).content
        soup = BeautifulSoup(html_doc, features='lxml')
        url_img = soup.find_all('span', {'class': 'cover'})[1].find_all('img')[0]['src']
        urllib.request.urlretrieve(url_img, filename)
