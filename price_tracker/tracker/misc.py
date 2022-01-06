def printError(err, function):
    print("Error: {0} in ".format(err) + function)

def parseFloat(floatStr):
    floatStr = floatStr.replace("R$ ", "").replace(",", ".")
    return float(floatStr)

def bestPriceDict(store, price):
    return {
        "store": store,
        "price": price
    }

def getBiggerValue(price1, price2):
    return price1 if price1["price"] > price2["price"] else price2