import time
import urllib.request
import datetime
import os
import errno
import logging
import argparse
import csv
import pkg_resources
import codecs

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()
    urls = []

    io = pkg_resources.resource_stream(__name__, "liste_urls.csv")
    utf8_reader = codecs.getreader("utf-8")
    c = csv.reader(utf8_reader(io))
    for row in c:
        urls.append(row)

    auj = datetime.datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Ajourd'hui : {auj}")

    i = 1

    for lien in urls:
        logger.info(lien)
        filename = "scrap_revuedepresse_simple/" + auj + "/" + str(i) + ".jpg"
        url = ''.join(lien)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        urllib.request.urlretrieve(url, filename)
        i += 1

    print("Temps d'exécution : %.2f secondes" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Scraper du site revue2presse. Version simplifiée.')
    parser.add_argument('--debug', help="Affiche les informations de déboguage", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()