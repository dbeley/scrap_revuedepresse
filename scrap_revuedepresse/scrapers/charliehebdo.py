import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_charliehebdo(url, filename):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    url = soup.find("img", {"class", "attachment-ch_300 size-ch_300"})[
        "srcset"
    ].split()[-2]
    urllib.request.urlretrieve(url, filename)
