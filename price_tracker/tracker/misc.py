import locale

def printError(err, function):
    print("Error: {0} in ".format(err) + function)

def parseRealToFloat(floatStr: str):
    # Kabum brings its prices with this
    floatStr = floatStr.replace("\xa0", "")
    
    floatStr = floatStr.replace(" ", "").replace(".", "")
    floatStr = floatStr.replace("R$", "").replace(",", ".")
    return float(floatStr)

def getFloatInCurrency(value: float):
    return locale.currency(value, grouping=True)