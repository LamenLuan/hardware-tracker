import locale
import time
from google.auth import exceptions
from tracker.scrapper import scrapper, getBestPrice
from tracker.misc import printError

def runScrapper():
    try:
        locale.setlocale(locale.LC_ALL, '')
        init = time.time()
        scrapper()
        end = time.time()
        print(f"Execution time: {round(end - init, 2)}s")
    # If cant communicate with Google sheets, I return the best price in console
    except exceptions.TransportError as err:
        printError("Connection error", "writePriceInSheet")
        print( getBestPrice() )

runScrapper()