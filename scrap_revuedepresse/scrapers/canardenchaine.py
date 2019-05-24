import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_canardenchaine(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    url = soup.find("img", {"alt": ""})["src"]
    urllib.request.urlretrieve(url, filename)
