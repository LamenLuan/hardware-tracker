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
    options.headless = True
    return webdriver.Firefox(options=options)

def prepareSeleniumSoup(url):
    driver = getDriver()
    try:
        driver.get(url)
        page = driver.page_source
        driver.close()
        return BeautifulSoup(page, "html.parser")
    except AttributeError as err: printError(err, "prepareSeleniumSoup")

def parseFloat(floatStr):
    floatStr = floatStr.replace("R$ ", "").replace(",", ".")
    return float(floatStr)

def bestPriceDict(store, price):
    return {
        "store": store,
        "price": price
    }

def getPichauPrice():
    soup = prepareSoup(pichauUrl)
    try:
        pichauClass = "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"
        mainDiv = soup.find("div", {"class": pichauClass})
        regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
        priceStr = regFinder.findall(str(mainDiv))[0][0]
        return bestPriceDict( "Pichau", parseFloat(priceStr) )
    except AttributeError as err: printError(err, "pichauPrice")

def getKabumPrice():
    soup = prepareSoup(kabumUrl)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("\xa0", " ")
        return bestPriceDict( "Kabum", parseFloat(priceStr) )
    except AttributeError as err: printError(err, "kabumPrice")

def getTerabytePrice():
    soup = prepareSeleniumSoup(terabyteUrl)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text
        return bestPriceDict( "Terabyte", parseFloat(priceStr) )
    except AttributeError as err: printError(err, "terabytePrice")

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
    date = datetime.today().date().strftime("%d/%m/%Y")
    time = datetime.today().time().strftime("%H:%M:%S")
    workSheet = spreadSheet.worksheet("BestPrice")
    cellList = workSheet.get_values("A:A")
    rowsWritten = len(cellList)
    bestPrice = getBestPrice()

    try:
        if cellList.count([date]) == 0:
            rowsWritten += 1
            workSheet.update(
                "A{0}:D{0}".format(rowsWritten),
                [ [ date, time, bestPrice["price"], bestPrice["store"] ] ],
                raw = False
            )
        else:
            lastPriceStr = workSheet.acell(f"B{rowsWritten}").value
            lastPrice = parseFloat(lastPriceStr)
            if bestPrice['price'] < lastPrice:
                workSheet.update(
                    "B{0}:D{0}".format(rowsWritten),
                    [ [ time, bestPrice['price'], bestPrice['store'] ] ],
                    raw = False
                )
                
    except TypeError or FileNotFoundError as err:
        printError(err, "writePriceInSheet")
    except gspread.SpreadsheetNotFound or gspread.WorksheetNotFound as err: 
        printError(err, "writePriceInSheet")
        

def runScrapper():
    try:
        writePriceInSheet()
    # If cant communicate with Google sheets, I return the best price in console
    except exceptions.TransportError as err:
        printError("Connection error", "writePriceInSheet")
        print( getBestPrice() )

runScrapper()