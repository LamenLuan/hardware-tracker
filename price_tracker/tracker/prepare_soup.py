from bs4 import BeautifulSoup
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

def prepareSoup(url: str):
    page = requests.get(url)
    if not page: page = cloudScrap(url)

    try: return BeautifulSoup(page.text, "html.parser")
    except AttributeError as err: printError(err, "prepareSoup")