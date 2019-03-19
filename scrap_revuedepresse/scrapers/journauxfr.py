import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_journauxfr(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features='lxml')
    url = soup.find('img', {'id': 'imageRevue'})['src']
    url = f"https://www.journaux.fr/{url}"
    urllib.request.urlretrieve(url, filename)
