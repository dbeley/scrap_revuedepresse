import cv2
import time
import urllib.request
import datetime
import os
import errno
import logging
import argparse
import pkg_resources
import codecs
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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
    # c = csv.reader(utf8_reader(io))
    # for row in c:
    #     urls.append(row)

    df = pd.read_csv(utf8_reader(io), sep=';')
    dict = df.to_dict(orient='records')
    # Lancement de selenium
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

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
                urllib.request.urlretrieve(url, filename)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "epresse":
            try:
                html_doc = requests.get(url).content
                soup = BeautifulSoup(html_doc, features='lxml')
                url = soup.find_all('span', {'class': 'cover'})[1].find_all('img')[0]['src']
                urllib.request.urlretrieve(url, filename)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "cnews":
            try:
                auj_cnews = datetime.datetime.now().strftime("%Y-%m-%d")
                browser.get(f"https://kiosque.cnews.fr/player/?q=NEP&d={auj_cnews}&c=CNEWS")
                time.sleep(8)
                browser.save_screenshot(filename)
                img = cv2.imread(filename)
                x, y = img.shape[1], img.shape[0]
                x1 = round(x/2)
                x2 = round(x*0.85)
                y1 = round(0.1*y)
                y2 = round(0.95*y)
                img_cropped = img[y1:y2, x1:x2]
                cv2.imwrite(filename, img_cropped)
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        elif source == "20m":
            try:
                auj_20m = datetime.datetime.now().strftime("%Y%m%d")
                année_20m = datetime.datetime.now().strftime("%Y")
                url_20m = f"https://pdf.20mn.fr/{année_20m}/quotidien/{auj_20m}_PAR.pdf"
                urllib.request.urlretrieve(url_20m, "20m.pdf")
                os.system("stapler sel 20m.pdf 1 20m1.pdf")
                # comment /etc/ImageMagick-7policy.xml
                os.system(f"convert -density 300 -trim 20m1.pdf -quality 100 {filename}")
                os.system("rm 20m.pdf 20m1.pdf")
            except Exception as e:
                logger.error(f"{source} : {str(e)}")
        else:
            logger.error(f"Méthode {source} non implémentée")

    browser.quit()

    logger.debug("Temps d'exécution : %.2f secondes" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description='Scraper revuedepresse.')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the url to parse (liste_journaux.csv or liste_journaux_weekend.csv", type=str)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
