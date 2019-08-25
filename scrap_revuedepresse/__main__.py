import time
import datetime
import logging
import locale
import argparse
import pkg_resources
import codecs
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .scrapers.revue2presse import scrap_revue2presse
from .scrapers.epresse import scrap_epresse
from .scrapers.journauxfr import scrap_journauxfr
from .scrapers.kiosko import scrap_kiosko
from .scrapers.cnews import scrap_cnews
from .scrapers.vingtminutes import scrap_vingtminutes
from .scrapers.canardenchaine import scrap_canardenchaine
from .scrapers.charliehebdo import scrap_charliehebdo
from .scrapers.courrierinternational import scrap_courrierinternational
from .scrapers.leun import scrap_leun
from .scrapers.lemonde import scrap_lemonde
from .scrapers.jeuneafrique import scrap_jeuneafrique

logger = logging.getLogger()
temps_debut = time.time()
locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")


def main():
    args = parse_args()
    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    if args.test:
        jour = "test"
    else:
        jour = datetime.datetime.now().strftime("%A")
    logger.debug("Aujourd'hui : %s", auj)
    logger.debug("Jour : %s", jour)

    directory = f"Images/{auj}/"
    if args.file is None:
        if args.international:
            io = pkg_resources.resource_stream(
                __name__, "liste_journaux_internationaux.csv"
            )
            directory = f"Images/{auj}_international/"
        else:
            io = pkg_resources.resource_stream(__name__, "liste_journaux.csv")
        utf8_reader = codecs.getreader("utf-8")
        file = utf8_reader(io)
    else:
        file = args.file
    try:
        df = pd.read_csv(file, sep=",", comment="#")
        dict = df.to_dict(orient="records")
    except Exception as e:
        logger.error("Erreur lecture %s : %s", args.file, e)
        exit()

    # Start selenium
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    # browser.set_page_load_timeout(60)

    ordre = 0
    for i in dict:
        if i[jour] == 1:
            ordre += 1
            méthode = i["Méthode"]
            url = i["URL"]
            titre = i["Titre"]
            filename = f"{directory}{str(ordre).zfill(2)}_{titre.replace(' ', '_')}.jpg"

            Path(directory).mkdir(parents=True, exist_ok=True)

            logger.info("%s : %s vers %s", méthode, url, filename)
            if méthode == "revue2presse":
                try:
                    scrap_revue2presse(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "epresse":
                try:
                    scrap_epresse(url, filename, auj)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "journauxfr":
                try:
                    scrap_journauxfr(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "kiosko":
                try:
                    scrap_kiosko(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "lemonde":
                try:
                    scrap_lemonde(url, filename, browser)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "cnews":
                try:
                    scrap_cnews(filename, browser)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "20m":
                try:
                    scrap_vingtminutes(filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "canardenchaine":
                try:
                    scrap_canardenchaine(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "charliehebdo":
                try:
                    scrap_charliehebdo(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "courrierinternational":
                try:
                    scrap_courrierinternational(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "jeuneafrique":
                try:
                    scrap_jeuneafrique(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            elif méthode == "leun":
                try:
                    scrap_leun(url, filename)
                except Exception as e:
                    logger.error("%s - %s : %s", titre, méthode, str(e))
            else:
                logger.error("%s : Méthode %s non implémentée", titre, méthode)
        else:
            logger.debug("%s : %s non extrait", i[jour], i["Titre"])

    browser.close()
    browser.quit()
    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrap newspapers covers for the revuedepresse bot."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File containing the urls to parse (optional, liste_journaux.csv by default)",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="Temporarily activates all the scrapers",
        dest="test",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--international",
        help="International version, use the liste_journaux_international.csv file",
        dest="international",
        action="store_true",
    )
    parser.set_defaults(test=False, international=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
