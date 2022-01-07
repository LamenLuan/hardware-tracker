import re
from tracker.prepare_soup import prepareSoup
from tracker.misc import printError, parseRealToFloat

def bestPriceDict(store: str, price: float):
    return {
        "store": store,
        "price": price
    }

def getKabumPrice(url: str):
    soup = prepareSoup(url)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("\xa0", " ")
        return bestPriceDict( "Kabum", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "getKabumPrice")

def getPichauPrice(url: str):
    soup = prepareSoup(url)
    try:
        pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"
        mainDiv = soup.find("div", {"class": pichauClass})
        regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
        priceStr = regFinder.findall(str(mainDiv))[0][0]
        return bestPriceDict( "Pichau", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "getPichauPrice")

def getTerabytePrice(url: str):
    soup = prepareSoup(url)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text
        return bestPriceDict( "Terabyte", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "getTerabytePrice")