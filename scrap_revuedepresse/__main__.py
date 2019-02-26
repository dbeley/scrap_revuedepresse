import time
import datetime
import os
import errno
import logging
import locale
import argparse
import pkg_resources
import codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .scrapers.revue2presse import scrap_revue2presse
from .scrapers.epresse import scrap_epresse
from .scrapers.journauxfr import scrap_journauxfr
from .scrapers.cnews import scrap_cnews
from .scrapers.vingtminutes import scrap_vingtminutes
from .scrapers.canardenchaine import scrap_canardenchaine
from .scrapers.charliehebdo import scrap_charliehebdo
from .scrapers.courrierinternational import scrap_courrierinternational
from .scrapers.leun import scrap_leun

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    liste_journaux = args.file
    if liste_journaux is None:
        logger.error("argument -f not defined. Exiting..")
        exit()
    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    jour = datetime.datetime.now().strftime("%A")
    # jour = "test"
    logger.debug(f"Aujourd'hui : {auj}")
    logger.debug(f"Jour : {jour}")
    directory = f"{auj}/"
    io = pkg_resources.resource_stream(__name__, liste_journaux)
    utf8_reader = codecs.getreader("utf-8")
    df = pd.read_csv(utf8_reader(io), sep=',')
    dict = df.to_dict(orient='records')

    # Lancement de selenium
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(10)

    for i in dict:
        if i[jour] == 1:
            filename = f"{directory}{str(i['Ordre']).zfill(2)}_{i['Titre'].replace(' ', '')}.jpg"

            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            méthode = i['Méthode']
            url = i['URL']
            logger.debug(f"{méthode} : {url} vers {filename}")
            if méthode == "revue2presse":
                try:
                    scrap_revue2presse(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "epresse":
                try:
                    scrap_epresse(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "journauxfr":
                try:
                    scrap_journauxfr(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "cnews":
                try:
                    scrap_cnews(filename, browser)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "20m":
                try:
                    scrap_vingtminutes(filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "canardenchaine":
                try:
                    scrap_canardenchaine(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "charliehebdo":
                try:
                    scrap_charliehebdo(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "courrierinternational":
                try:
                    scrap_courrierinternational(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            elif méthode == "leun":
                try:
                    scrap_leun(url, filename)
                except Exception as e:
                    logger.error(f"{méthode} : {str(e)}")
            else:
                logger.error(f"Méthode {méthode} non implémentée")
        else:
            logger.debug(f"{i[jour]} : {i['Titre']} non extrait")

    browser.quit()
    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Scraper revuedepresse.')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the urls to parse (liste_journaux.csv by default)", type=str, default="liste_journaux.csv")
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
