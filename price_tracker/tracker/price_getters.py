import re

from bs4 import BeautifulSoup
from tracker.prepare_soup import prepareSoup
from tracker.misc import printError, parseRealToFloat

def bestPriceDict(name: str, store: str, price: float):
    return {
        "name": name,
        "store": store,
        "price": price
    }

def getKabumPrice(url: str):
    soup = prepareSoup(url)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("\xa0", " ")
        name = soup.find("h1", itemprop="name").text
        return bestPriceDict(name, "Kabum", parseRealToFloat(priceStr))
    except AttributeError as err: printError(err, "getKabumPrice")

def getPichauPriceStr(soup: BeautifulSoup):
    pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"
    mainDiv = soup.find("div", {"class": pichauClass})
    regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
    return regFinder.findall(str(mainDiv))[0][0]

def getPichauPrice(url: str):
    soup = prepareSoup(url)
    try:
        priceStr = getPichauPriceStr(soup)
        name = soup.find("h1", {"data-cy":"product-page-title"}).text
        return bestPriceDict(name, "Pichau", parseRealToFloat(priceStr))
    except AttributeError as err: printError(err, "getPichauPrice")

def getTerabytePrice(url: str):
    soup = prepareSoup(url)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text
        name = soup.find("h1", {"class": "tit-prod"}).text
        return bestPriceDict(name, "Terabyte", parseRealToFloat(priceStr))
    except AttributeError as err: printError(err, "getTerabytePrice")