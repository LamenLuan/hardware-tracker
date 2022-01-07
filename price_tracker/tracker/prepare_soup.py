from bs4 import BeautifulSoup
from tracker.misc import printError
import requests
import cloudscraper

def cloudScrap(url):
    for i in range(30):
        try:
            scraper = cloudscraper.create_scraper()
            return scraper.get(url)
        except cloudscraper.exceptions.CloudflareChallengeError: continue

def prepareSoup(url):
    page = requests.get(url)
    if not page: page = cloudScrap(url)

    try: return BeautifulSoup(page.text, "html.parser")
    except AttributeError as err: printError(err, "prepareSoup")