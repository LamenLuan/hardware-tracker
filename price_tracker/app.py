from google.auth import exceptions
from tracker.scrapper import scrapper, getBestPrice
from tracker.misc import printError

def runScrapper():
    try:
        scrapper()
    # If cant communicate with Google sheets, I return the best price in console
    except exceptions.TransportError as err:
        printError("Connection error", "writePriceInSheet")
        print( getBestPrice() )

runScrapper()