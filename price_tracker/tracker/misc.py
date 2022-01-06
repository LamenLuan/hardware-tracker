def printError(err, function):
    print("Error: {0} in ".format(err) + function)

def parseRealToFloat(floatStr):
    floatStr = floatStr.replace("R$ ", "").replace(",", ".")
    return float(floatStr)