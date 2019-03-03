import urllib.request
from bs4 import BeautifulSoup
from time import sleep


def scrap_lemonde(url, filename, browser):
    browser.get(url)
    sleep(5)
    html_doc = browser.page_source
    soup = BeautifulSoup(html_doc, features='lxml')
    url = soup.find_all('img')[1]['src']
    urllib.request.urlretrieve(url, filename)
