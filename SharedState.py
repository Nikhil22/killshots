import math
from collections import defaultdict

_histories = {}

def updateHistory(key, value):
    _histories[str(key)] = value
    
def getHistory(key):
    return _histories[str(key)]
        
 
_stopLossPrices = {}

def updateStopLossPrice(key, value):
    _stopLossPrices[str(key)] = value
    
def getStopLossPrice(key):
    return _stopLossPrices[str(key)]
    

_takeProfitPrices = {}

def updateTakeProfitPrice(key, values, multiple):
    entry = values[0]
    stopLoss = values[1]
    diff = entry - stopLoss
    takeProfitPrice = diff * multiple + entry
    _takeProfitPrices[str(key)] = takeProfitPrice

def getTakeProfitPrice(key):
    return _takeProfitPrices[str(key)]

    
_entryPrices = {}

def updateEntryPrice(key, value):
    _entryPrices[str(key)] = value
    
def getEntryPrice(key):
    return _entryPrices[str(key)]

    
def calculateQuantity(entryPrice, stopLossPrice, maxStake):
    diff = entryPrice - stopLossPrice
    if diff == 0:
        return 0
    return math.floor(maxStake/diff)
 
def calculateQuantityConservative(entryPrice, maxStake):
     return math.floor(maxStake/entryPrice)

_symbolsWithOpenOrders = set()
 
def addToSymbolsWithOpenOrders(value):
    _symbolsWithOpenOrders.add(value)
    
def getSymbolsWithOpenOrders():
    return _symbolsWithOpenOrders
