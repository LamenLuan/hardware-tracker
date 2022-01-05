from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
import gspread
from datetime import date

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
        return float(priceStr)
    except AttributeError as err: printError(err, "pichauPrice")

def getKabumPrice():
    soup = prepareSoup(kabumUrl)
    try:
        priceTag = soup.find("h4", itemprop="price")
        priceStr = priceTag.text.replace("R$\xa0", "").replace(",", ".")
        return float(priceStr)
    except AttributeError as err: printError(err, "kabumPrice")

def getTerabytePrice():
    soup = prepareSeleniumSoup(terabyteUrl)
    try:
        priceTag = soup.find("p", id="valVista")
        priceStr = priceTag.text.replace("R$ ", "").replace(",", ".")
        return float(priceStr)
    except AttributeError as err: printError(err, "terabytePrice")

def bestPriceDict(store, price):
    return {
        "store": store,
        "price": price
    }

def getBestPrice():
    kabumPrice = getKabumPrice()
    pichauPrice = getPichauPrice()
    terabytePrice = getTerabytePrice()

    if(kabumPrice < pichauPrice and kabumPrice < terabytePrice):
        if(kabumPrice): return bestPriceDict("Kabum", kabumPrice)
    elif(pichauPrice < terabytePrice):
        if(pichauPrice): return bestPriceDict("Pichau", pichauPrice)
    elif(terabytePrice): return bestPriceDict("Terabyte", terabytePrice)

def writePriceInSheet():
    serviceAccount = gspread.service_account("gspread\\account_key.json")
    spreadSheet = serviceAccount.open("tracking-sheet")
    dateToday = date.today().isoformat()
    workSheet = spreadSheet.worksheet("BestPrice")
    cellList = workSheet.get_values("A:A")

    if cellList.count([dateToday]) == 0:
        try:
            bestPrice = getBestPrice()
            # New line index
            i = len(cellList) + 1
            workSheet.update(
                f"A{i}:C{i}",
                [ [dateToday, bestPrice["price"], bestPrice["store"]] ],
                raw=False
            )
        except TypeError as err:
            printError(err, "writePriceInSheet")
            return
    else: print(f"Warning: Date '{dateToday}' already tracked")

def runScrapper():
    try:
        writePriceInSheet()
    # If I cant communicate with Google sheets, I return the best price in console
    except gspread.SpreadsheetNotFound as err: 
        print( getBestPrice() )
        printError(err, "writePriceInSheet")
    except gspread.WorksheetNotFound as err:
        printError(err, "writePriceInSheet")

runScrapper()