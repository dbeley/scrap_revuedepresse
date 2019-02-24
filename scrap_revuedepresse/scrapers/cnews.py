import cv2
import time
import datetime


def scrap_cnews(filename, browser):
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
