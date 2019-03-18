import os
import datetime
import urllib.request


def scrap_vingtminutes(filename):
    auj_20m = datetime.datetime.now().strftime("%Y%m%d")
    année_20m = datetime.datetime.now().strftime("%Y")
    url_20m = f"https://pdf.20mn.fr/{année_20m}/quotidien/{auj_20m}_PAR.pdf"
    urllib.request.urlretrieve(url_20m, "20m.pdf")
    os.system("stapler sel 20m.pdf 1 20m1.pdf")
    # change /etc/ImageMagick-7policy.xml and add to policy
    # <policy domain="coder" rights="read | write" pattern="PDF" />
    os.system(f"convert -density 300 -trim 20m1.pdf -quality 100 {filename}")
    os.system("rm 20m.pdf 20m1.pdf")
