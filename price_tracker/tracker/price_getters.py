import re
from bs4 import BeautifulSoup
from tracker.prepare_soup import prepareSoup
from tracker.misc import parseRealToFloat

pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"

def bestPriceDict(name: str, store: str, cash: float, onTime: float):
    return {
        "name": name,
        "store": store,
        "cash": cash,
        "onTime": onTime
    }

def getKabumPrice(url: str):
    soup = prepareSoup(url)
    try:
        cash = soup.find("h4", itemprop="price").text
        cash = parseRealToFloat(cash)
        onTime = soup.find("b", {"class": "regularPrice"}).text
        onTime = parseRealToFloat(onTime)
        name = soup.find("h1", itemprop="name").text
        return bestPriceDict(name, "Kabum", cash, onTime)
    except AttributeError: None

def getPichauPriceStr(soup: BeautifulSoup):
    mainDiv = soup.find("div", {"class": pichauClass}).text
    regFinder = re.compile("([0-9]+(.[0-9]+)*,[0-9]{2})")
    findResult = regFinder.findall(mainDiv)
    return {"cash": findResult[0][0], "onTime": findResult[1][0]}

def checkPichauOutOfStock(soup: BeautifulSoup):
    outOfStock = {"content": "outofstock", "property": "product:availability"}
    return soup.find("meta", outOfStock) is not None

def getPichauPrice(url: str):
    soup = prepareSoup(url)
    try:
        if checkPichauOutOfStock(soup): return None
        prices = getPichauPriceStr(soup)
        cash = parseRealToFloat(prices["cash"])
        onTime = parseRealToFloat(prices["onTime"])
        name = soup.find("h1", {"data-cy":"product-page-title"}).text
        return bestPriceDict(name, "Pichau", cash, onTime)
    except AttributeError: None

def getTeraPrice(url: str):
    soup = prepareSoup(url)
    try:
        cash = soup.find("p", id="valVista").text
        cash = parseRealToFloat(cash)
        onTime = soup.find_all("span", id="valParc")[1].text
        onTime = parseRealToFloat(onTime)
        name = soup.find("h1", {"class": "tit-prod"}).text
        return bestPriceDict(name, "Terabyte", cash, onTime)
    except AttributeError: None

def getGkPrice(url: str):
    soup = prepareSoup(url)
    try:
        prices = soup.find_all("span", {"class": "total"})
        cash = prices[1].text
        cash = parseRealToFloat(cash)
        onTime = prices[0].text
        onTime = parseRealToFloat(onTime)
        name = soup.find("h1", {"class": "h1 m-0"}).text.strip()
        return bestPriceDict(name, "GK Infostore", cash, onTime)
    except AttributeError: None

getters = {
    "kabum": getKabumPrice,
    "pichau": getPichauPrice,
    "terabyteshop": getTeraPrice,
    "gkinfostore": getGkPrice
}