# scrap_revuedepresse

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6a62746ff508448aadf4eb2c43dfb53e)](https://app.codacy.com/app/dbeley/scrap_revuedepresse?utm_source=github.com&utm_medium=referral&utm_content=dbeley/scrap_revuedepresse&utm_campaign=Badge_Grade_Dashboard)

Extract newspaper covers from a variety of sources.

The extracted images will be placed under an Images folder in a folder named after the current date (i.e. 2019-07-31). 

The international version will be placed in a directory with "_international" append to its name (i.e. 2019-07-31_international).

The newspaper covers urls are set in the liste_journaux.csv file in the package source directory.

## Requirements

- firefox
- geckodriver
- stapler
- imagemagick (convert pdf to image)
- ghostscript (imagemagick pdf support)

Python librairies :

- lxml
- urllib3
- bs4
- requests
- pandas
- selenium
- opencv-python

## Installation

Installation in a virtualenv with pip (recommended)

```
pipenv install '-e .'
```

Standard installation (you will have to modify the systemd service to match this install)

```
python setup.py install
```

## Usage

```
scrap_revuedepresse
scrap_revuedepresse --international
scrap_revuedepresse -f custom.csv
```

### As a Systemd Service

```
cp systemd-service/* ~/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable --now scrap_revuedepresse.timer
systemctl --user enable --now scrap_revuedepresse_inter.timer
systemctl --user start scrap_revuedepresse
```

## Help

```
scrap_revuedepresse -h
```

```
usage: scrap_revuedepresse [-h] [--debug] [-f FILE] [-t] [-i]

Scrap newspapers covers for the revuedepresse bot.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -f FILE, --file FILE  File containing the urls to parse (optional,
                        liste_journaux.csv by default)
  -t, --test            Temporarily activates all the scrapers
  -i, --international   International version, use the
                        liste_journaux_international.csv file
```

## Autostarting

Systemd services and their respective timers are provided in the systemd-service/ folder for both the standard and the international versions of the script.

After copying the service and timer files in ~/.config/systemd/user/, you can launch the timer with :

```
systemctl --user daemon-reload
systemctl --user enable --now scrap_revuedepresse.timer
systemctl --user enable --now scrap_revuedepresse_inter.timer
```
