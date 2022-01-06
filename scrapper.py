from bs4 import BeautifulSoup
import re
from google.auth import exceptions
import requests
from selenium import webdriver
import gspread
from datetime import datetime

kabumUrl = "https://www.kabum.com.br/produto/115318/headset-gamer-hyperx-cloud-core-som-surround-7-1-drivers-53mm-usb-e-p3-hx-hscc-2-bk-ww"
pichauUrl = "https://www.pichau.com.br/headset-gamer-hyperx-cloud-core-som-surround-7-1-drivers-53mm-preto-hx-hscc-2-bk-ww"
terabyteUrl = "https://www.terabyteshop.com.br/produto/18711/headset-gamer-hyperx-cloud-core-surround-71-35mm-ou-usb-black-hx-hscc-2-bkww"

def printError(err, function):
    print("Error: {0} in ".format(err) + function)

def prepareSoup(url):
    page = requests.get(url)
    try: return BeautifulSoup(page.text, "html.parser")
    except AttributeError as err: printError(err, "prepareSoup")
   
def getDriver():
    options = webdriver.FirefoxOptions()
    options.headless = True;
    return webdriver.Firefox(options=options)

def prepareSeleniumSoup(url):
    driver = getDriver()
    try:
        driver.get(url)
        page = driver.page_source
        driver.close()
        return BeautifulSoup(page, "html.parser")
    except AttributeError as err: printError(err, "prepareSeleniumSoup")

def getPichauPrice():
    soup = prepareSoup(pichauUrl)
    try:
        pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"
        mainDiv = soup.find("div", {"class": pichauClass})
        regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
        priceStr = regFinder.findall(str(mainDiv))[0][0].replace(",", ".")
        return bestPriceDict("Pichau", float(priceStr))
    except AttributeError as err: printError(err, "pichauPrice")

def getKabumPrice():
    soup = prepareSoup(kabumUrl)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("R$\xa0", "").replace(",", ".")
        return bestPriceDict("Kabum", float(priceStr))
    except AttributeError as err: printError(err, "kabumPrice")

def getTerabytePrice():
    soup = prepareSeleniumSoup(terabyteUrl)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text.replace("R$ ", "").replace(",", ".")
        return bestPriceDict("Terabyte", float(priceStr))
    except AttributeError as err: printError(err, "terabytePrice")

def bestPriceDict(store, price):
    return {
        "store": store,
        "price": price
    }

def getBiggerValue(price1, price2):
    return price1 if price1["price"] > price2["price"] else price2

def getBestPrice():
    prices = [ getKabumPrice(), getPichauPrice(), getTerabytePrice() ]
    try:
        for price in prices: prices.remove(None)
    except:
        if len(prices) == 0: return None
    while len(prices) > 1:
        biggerValue = getBiggerValue(prices[0], prices[1])
        prices.remove(biggerValue)
    return prices[0]


def writePriceInSheet():
    serviceAccount = gspread.service_account("gspread\\account_key.json")
    spreadSheet = serviceAccount.open("tracking-sheet")
    dateToday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    workSheet = spreadSheet.worksheet("BestPrice")
    cellList = workSheet.get_values("A:A")

    try:
        bestPrice = getBestPrice()
        # New line index
        i = len(cellList) + 1
        workSheet.update(
            f"A{i}:C{i}",
            [ [ dateToday, bestPrice["price"], bestPrice["store"] ] ],
            raw=False
        )
    except TypeError as err:
        printError(err, "writePriceInSheet")
        return

def runScrapper():
    try:
        writePriceInSheet()
        return
    # If cant communicate with Google sheets, I return the best price in console
    except gspread.SpreadsheetNotFound or gspread.WorksheetNotFound as err: 
        printError(err, "writePriceInSheet")
    except FileNotFoundError as err:
        printError(err, "writePriceInSheet")
    except exceptions.TransportError as err:
        printError("Connection error", "writePriceInSheet")
    print( getBestPrice() )

runScrapper()