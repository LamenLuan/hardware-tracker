import locale
from google.auth import exceptions
from tracker.scrapper import scrapper, getBestPrice
from tracker.misc import printError
from multiprocessing import freeze_support

def runScrapper():
    try:
        locale.setlocale(locale.LC_ALL, '')
        print(f"Execution time: {round(scrapper(), 2)}s")
    except TypeError as err:
        printError(err, "writePriceInSheet")
    # If cant communicate with Google sheets, I return the best price in console
    except exceptions.TransportError as err:
        printError("Connection error", "writePriceInSheet")
        print( getBestPrice() )

if __name__ == '__main__':
    freeze_support()
    runScrapper()