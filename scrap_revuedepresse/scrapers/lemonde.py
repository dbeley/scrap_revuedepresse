import urllib.request
from bs4 import BeautifulSoup


def scrap_lemonde(url, filename, browser):
    browser.get(url)
    html_doc = browser.page_source
    soup = BeautifulSoup(html_doc, features='lxml')
    url = soup.find_all('img')[1]['src']
    urllib.request.urlretrieve(url, filename)
