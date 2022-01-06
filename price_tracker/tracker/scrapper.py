import gspread
from datetime import datetime
from tracker.price_getters import *
from tracker.misc import printError, parseFloat, getBiggerValue

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


def scrapper():
    serviceAccount = gspread.service_account("..\gspread\\account_key.json")
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
            lastPriceStr = workSheet.acell(f"C{rowsWritten}").value
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
