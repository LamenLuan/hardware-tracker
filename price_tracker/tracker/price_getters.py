import re
from tracker.prepare_soup import prepareSoup
from tracker.misc import printError, parseRealToFloat

kabumUrl = "https://www.kabum.com.br/produto/115318/headset-gamer-hyperx-cloud-core-som-surround-7-1-drivers-53mm-usb-e-p3-hx-hscc-2-bk-ww"
pichauUrl = "https://www.pichau.com.br/headset-gamer-hyperx-cloud-core-som-surround-7-1-drivers-53mm-preto-hx-hscc-2-bk-ww"
terabyteUrl = "https://www.terabyteshop.com.br/produto/18711/headset-gamer-hyperx-cloud-core-surround-71-35mm-ou-usb-black-hx-hscc-2-bkww"

def bestPriceDict(store, price):
    return {
        "store": store,
        "price": price
    }

def getKabumPrice():
    soup = prepareSoup(kabumUrl)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("\xa0", " ")
        return bestPriceDict( "Kabum", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "kabumPrice")

def getPichauPrice():
    soup = prepareSoup(pichauUrl)
    try:
        pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"
        mainDiv = soup.find("div", {"class": pichauClass})
        regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
        priceStr = regFinder.findall(str(mainDiv))[0][0]
        return bestPriceDict( "Pichau", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "pichauPrice")

def getTerabytePrice():
    soup = prepareSoup(terabyteUrl)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text
        return bestPriceDict( "Terabyte", parseRealToFloat(priceStr) )
    except AttributeError as err: printError(err, "terabytePrice")