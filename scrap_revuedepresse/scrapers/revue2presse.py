import urllib.request


def scrap_revue2presse(url, filename):
    urllib.request.urlretrieve(url, filename)
