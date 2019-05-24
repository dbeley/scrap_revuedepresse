import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_kiosko(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    url_img = soup.find("div", {"class": "frontPageImage"}).find("img")["src"]
    urllib.request.urlretrieve(url_img, filename)
