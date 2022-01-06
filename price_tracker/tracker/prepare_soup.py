from bs4 import BeautifulSoup
from selenium import webdriver
from tracker.misc import printError
import requests

def getDriver():
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(options=options)

def prepareSoup(url):
    page = requests.get(url)
    try: return BeautifulSoup(page.text, "html.parser")
    except AttributeError as err: printError(err, "prepareSoup")

def prepareSeleniumSoup(url):
    driver = getDriver()
    try:
        driver.get(url)
        page = driver.page_source
        driver.close()
        return BeautifulSoup(page, "html.parser")
    except AttributeError as err: printError(err, "prepareSeleniumSoup")