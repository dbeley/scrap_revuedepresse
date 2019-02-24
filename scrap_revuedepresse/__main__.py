import time
import datetime
import os
import errno
import logging
import argparse
import pkg_resources
import codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .scrapers.cnews import scrap_cnews
from .scrapers.epresse import scrap_epresse
from .scrapers.revue2presse import scrap_revue2presse
from .scrapers.vingtminutes import scrap_vingtminutes

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    liste_journaux = args.file
    if liste_journaux is None:
        logger.error("argument -f not defined. Exiting..")
        exit()
    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    logger.debug(f"Aujourd'hui : {auj}")
    directory = f"{auj}/"
    io = pkg_resources.resource_stream(__name__, liste_journaux)
    utf8_reader = codecs.getreader("utf-8")
    df = pd.read_csv(utf8_reader(io), sep=';')
    dict = df.to_dict(orient='records')

    # Lancement de selenium
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(10)

    for i in dict:
        filename = f"{directory}{str(i['ID']).zfill(2)}_{i['Titre'].replace(' ', '')}.jpg"
        logger.debug(filename)

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        source = i['Source']
        url = i['URL']
        if source == "revue2presse":
            try:
                scrap_revue2presse(url, filename)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "epresse":
            try:
                scrap_epresse(url, filename)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "cnews":
            try:
                scrap_cnews(filename, browser)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "20m":
            try:
                scrap_vingtminutes(filename)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        else:
            logger.error(f"Méthode {source} non implémentée")

    browser.quit()

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Scraper revuedepresse.')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the url to parse (liste_journaux.csv or liste_journaux_weekend.csv", type=str)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
