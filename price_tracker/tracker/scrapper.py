import gspread
from datetime import datetime

from gspread.worksheet import Worksheet
from tracker.price_getters import *
from tracker.misc import printError, parseRealToFloat
from win10toast import ToastNotifier

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

def checkIfBestPriceEver(price: float, workSheet: Worksheet, rowsWritten: int):
    bestPrice = True
    for i in range(rowsWritten - 1):
        rowStr = workSheet.cell(i + 2, 3).value
        rowPrice = parseRealToFloat(rowStr)
        if price >= rowPrice:
            bestPrice = False
            break
    return bestPrice

def sendNotification(bestPrice):
    preco = bestPrice['price']
    store = bestPrice['store']
    toaster = ToastNotifier()
    toaster.show_toast(
        title = "Novo melhor preço!",
        msg = f"O produto está por R$ {preco} na {store}",
        duration=30
    )

def scrapper():
    serviceAccount = gspread.service_account("..\gspread\\account_key.json")
    spreadSheet = serviceAccount.open("tracking-sheet")
    date = datetime.today().date().strftime("%d/%m/%Y")
    time = datetime.today().time().strftime("%H:%M:%S")
    workSheet = spreadSheet.worksheet("BestPrice")
    cellList = workSheet.get_values("A:A")
    rowsWritten = len(cellList)
    bestPrice = getBestPrice()
    notify = checkIfBestPriceEver(bestPrice['price'], workSheet, rowsWritten)
        
    try:
        if cellList.count([date]) == 0:
            rowsWritten += 1
            workSheet.update(
                "A{0}:D{0}".format(rowsWritten),
                [ [ date, time, bestPrice["price"], bestPrice["store"] ] ],
                raw = False
            )
        else:
            lastPriceStr = workSheet.acell(f"C{rowsWritten}").value
            lastPrice = parseRealToFloat(lastPriceStr)
            if bestPrice['price'] < lastPrice:
                workSheet.update(
                    "B{0}:D{0}".format(rowsWritten),
                    [ [ time, bestPrice['price'], bestPrice['store'] ] ],
                    raw = False
                )
        if notify: sendNotification(bestPrice)

    except TypeError or FileNotFoundError as err:
        printError(err, "writePriceInSheet")
    except gspread.SpreadsheetNotFound or gspread.WorksheetNotFound as err: 
        printError(err, "writePriceInSheet")