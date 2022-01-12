from bs4 import BeautifulSoup
from requests.adapters import Response
from tracker.misc import printError
import requests
import cloudscraper

cloudRepeatNumber = 30

def cloudScrap(url: str):
    for i in range(cloudRepeatNumber):
        try:
            scraper = cloudscraper.create_scraper()
            return scraper.get(url)
        except cloudscraper.exceptions.CloudflareChallengeError: continue

def getSoup(page: Response):
    try: return BeautifulSoup(page.text, "html.parser")
    except AttributeError as err: printError(err, "getSoup")

def prepareSoup(url: str):
    page = requests.get(url)
    if not page: page = cloudScrap(url)
    return getSoup(page)