import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import datetime
import os
import errno
import logging
import argparse
import csv

logger = logging.getLogger()
temps_debut = time.time()


def main(args):
    url_base = "http://www.revue2presse.fr"
    url_depart = url_base + "/presse/quotidien"
    html_doc = requests.get(url_depart).content
    soup = BeautifulSoup(html_doc, features="lxml")

    urls = []

    # Nom utilisé : champ 'alt' de l'image
    blacklist = ["Les Echos",
                 "Sud Ouest",
                 "L'Est Républicain",
                 "Corse Matin",
                 "Le Dauphiné Libéré",
                 "Le Républicain Lorrain",
                 "Dernières Nouvelles d'Alsace",
                 "L'Est Eclair",
                 "Le Télégramme",
                 "Libération Champagne",
                 ]

    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Ajourd'hui : {auj}")

    # url_depart
    for content in soup.find_all("div", {"id": "left-large-4"}):
        logger.debug(content)
        # Magazines présents sur url_depart
        for mag in content.find_all("li"):
            logger.debug(mag)
            # Lien du magazine (normalement un)
            for lien in mag.find_all("a", href=True):
                logger.debug(lien)
                url_mag = url_base + lien['href']
                mag_requests = requests.get(url_mag).content
                mag_soup = BeautifulSoup(mag_requests, features="lxml")
                # Page dédiée au magazine
                for a in mag_soup.find_all("a", href=True):
                    logger.debug(a)
                    # Lien image
                    for img in a.find_all("img", {"class": "cover"}):
                        logger.debug(img)
                        if img['alt'] not in blacklist:
                            logger.info(f"{img['alt']}")
                            lien_img = url_base + img['src']
                            filename = auj + "/" + img['alt'] + ".jpg"
                            if not os.path.exists(os.path.dirname(filename)):
                                try:
                                    os.makedirs(os.path.dirname(filename))
                                except OSError as exc:
                                    if exc.errno != errno.EEXIST:
                                        raise
                            urllib.request.urlretrieve(lien_img, filename)
                            urls.append(lien_img)
                        else:
                            logger.warning(f"{img['alt']} est blacklisté")

    # Export des liens
    with open("liste_urls.csv", 'w') as file:
        for row in urls:
            file.write(row)
            file.write("\n")
    print("Temps d'exécution : %.2f secondes" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Scraper du site revue2presse')
    parser.add_argument('--debug', help="Affiche les informations de déboguage", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main(parse_args())
