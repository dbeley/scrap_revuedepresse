import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_courrierinternational(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    url = soup.find("img", {"class": "weekly-cover"})["data-srcset"].split()[
        -2
    ]
    urllib.request.urlretrieve(url, filename)
