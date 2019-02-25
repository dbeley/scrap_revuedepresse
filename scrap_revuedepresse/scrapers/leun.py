import urllib.request
import requests
from bs4 import BeautifulSoup


def scrap_leun(url, filename):
    urllib.request.urlretrieve(url, filename)
