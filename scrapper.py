from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver

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

def pichauPrice():
    soup = prepareSoup(pichauUrl)
    try:
        mainDiv = soup.find("div", {"class": "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-5"})
        regFinder = re.compile("R\$<!-- -->([0-9]+(.[0-9]+)*,[0-9]{2})")
        return regFinder.findall(str(mainDiv))[0][0]
    except AttributeError as err: printError(err, "pichauPrice")

def kabumPrice():
    soup = prepareSoup(kabumUrl)
    try:
        priceTag = soup.find("h4", itemprop="price")
        return priceTag.text.replace("R$\xa0", "")
    except AttributeError as err: printError(err, "kabumPrice")

def terabytePrice():
    soup = prepareSeleniumSoup(terabyteUrl)
    try:
        priceTag = soup.find("p", id="valVista")
        return priceTag.text.replace("R$ ", "")
    except AttributeError as err: printError(err, "terabytePrice")

print( "Kabum: R$ " + kabumPrice() )
print( "Pichau: R$ " + pichauPrice() )
print( "Terabyte: R$ " + terabytePrice() )