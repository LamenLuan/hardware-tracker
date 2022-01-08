import time
import json
import locale
import gspread
from io import TextIOWrapper
from datetime import datetime
from gspread.worksheet import Worksheet
from tracker.price_getters import *
from tracker.misc import printError, parseRealToFloat
from win10toast import ToastNotifier

def getBiggerValue(price1: dict, price2: dict):
    return price1 if price1["price"] > price2["price"] else price2

def CheckIfValidSite(site: str, priceList: list):
    regFinder = re.compile("https://www.([A-Za-z0-9]+)")
    siteName = regFinder.findall(site)[0]

    if siteName == "kabum": priceList.append( getKabumPrice(site) ) 
    elif siteName == "pichau": priceList.append( getPichauPrice(site) )
    elif siteName == "terabyteshop": priceList.append( getTerabytePrice(site) )

def PricesFromSites(file: TextIOWrapper):
    prices = []
    sites = json.load(file)
    for site in sites: CheckIfValidSite(site, prices)
    return prices

def getBestPrice():
    file = open("..\sites.json", "r")
    prices = PricesFromSites(file)

    try:
        for price in prices: prices.remove(None)
    except:
        if len(prices) == 0: return None
    while len(prices) > 1:
        biggerValue = getBiggerValue(prices[0], prices[1])
        prices.remove(biggerValue)

    return prices[0]

def checkIfBestPriceEver(price: float, workSheet: Worksheet):
    bestPrice = parseRealToFloat(workSheet.cell(2, 6).value)
    if bestPrice is None or price < bestPrice:
        workSheet.update_cell(2, 6, price) 
        return True
    return False

def sendNotification(bestPrice: dict):
    precoStr = locale.currency(bestPrice['price'], grouping=True)
    store = bestPrice['store']
    toaster = ToastNotifier()
    toaster.show_toast(
        title = "Novo melhor preço!",
        msg = f"O produto está por {precoStr} na {store}",
        duration=15
    )

def scrapper():
    init = time.time()
    serviceAccount = gspread.service_account("..\gspread\\account_key.json")
    spreadSheet = serviceAccount.open("tracking-sheet")
    dateStr = datetime.today().date().isoformat()
    timeStr = datetime.today().time().strftime("%H:%M:%S")
    workSheet = spreadSheet.worksheet("BestPrice")
    cellList = workSheet.get_values("A:A")
    rowsWritten = len(cellList)
    bestPrice = getBestPrice()
    notify = checkIfBestPriceEver(bestPrice['price'], workSheet)
        
    try:
        if cellList.count([dateStr]) == 0:
            rowsWritten += 1
            workSheet.update(
                "A{0}:D{0}".format(rowsWritten),
                [ [dateStr, timeStr, bestPrice["price"], bestPrice["store"]] ],
                raw = False
            )
        else:
            lastPriceStr = workSheet.acell(f"C{rowsWritten}").value
            lastPrice = parseRealToFloat(lastPriceStr)
            if bestPrice['price'] < lastPrice:
                workSheet.update(
                    "B{0}:D{0}".format(rowsWritten),
                    [ [ timeStr, bestPrice['price'], bestPrice['store'] ] ],
                    raw = False
                )
        end = time.time()
        if notify: sendNotification(bestPrice)

    except TypeError or FileNotFoundError as err:
        printError(err, "writePriceInSheet")
    except gspread.SpreadsheetNotFound or gspread.WorksheetNotFound as err: 
        printError(err, "writePriceInSheet")

    return end - init