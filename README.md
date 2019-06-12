# scrap_revuedepresse

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6a62746ff508448aadf4eb2c43dfb53e)](https://app.codacy.com/app/dbeley/scrap_revuedepresse?utm_source=github.com&utm_medium=referral&utm_content=dbeley/scrap_revuedepresse&utm_campaign=Badge_Grade_Dashboard)

Scrap newspaper covers from a variety of sources.

## Requirements

- lxml
- urllib3
- bs4
- requests
- pandas
- selenium
- opencv-python
- stapler
- imagemagick (convert pdf to image)
- ghostscript (imagemagick pdf support)

## Installation in a virtualenv

```
pipenv install '-e .'
```

## Usage

```
scrap_revuedepresse
scrap_revuedepresse --international
scrap_revuedepresse -f custom.csv
```

## Help

```
scrap_revuedepresse -h
```

```
usage: scrap_revuedepresse [-h] [--debug] [-f FILE] [-t] [-i]

Scraper revuedepresse.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -f FILE, --file FILE  File containing the urls to parse (optional,
                        liste_journaux.csv by default)
  -t, --test            Temporary activates all the scrapers
  -i, --international   International version, use the
                        liste_journaux_international.csv file
```
