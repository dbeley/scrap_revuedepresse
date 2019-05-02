# scrap_revuedepresse

Scrap newspaper covers from a variety of sources.

## Requirements

- python-lxml
- python-urllib3
- python-beautifulsoup4
- python-requests
- python-selenium
- geckodriver
- firefox
- opencv
- stapler
- python-pandas
- hdf5
- imagemagick (convert pdf to image)
- ghostscript (imagemagick pdf support)

## Installation

```
pipenv install '-e .'
```

## Usage

```
pipenv run scrap_revuedepresse
pipenv run scrap_revuedepresse --international
pipenv run scrap_revuedepresse -f custom.csv
```

## Help

```
scrap_revuedepresse -h
```
