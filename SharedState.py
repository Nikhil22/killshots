import math
from collections import defaultdict

_histories = {}

def updateHistory(key, value):
    _histories[str(key)] = value
    
def getHistory(key):
    return _histories.get(str(key))
        
 
_stopLossPrices = {}

def updateStopLossPrice(key, value):
    _stopLossPrices[str(key)] = value
    
def getStopLossPrice(key):
    return _stopLossPrices.get(str(key))
    

_takeProfitPrices = {}

def updateTakeProfitPrice(key, values, multiple):
    entry = values[0]
    stopLoss = values[1]
    diff = entry - stopLoss
    takeProfitPrice = diff * multiple + entry
    _takeProfitPrices[str(key)] = takeProfitPrice

def getTakeProfitPrice(key):
    return _takeProfitPrices.get(str(key))

    
_entryPrices = {}

def updateEntryPrice(key, value):
    _entryPrices[str(key)] = value
    
def getEntryPrice(key):
    return _entryPrices.get(str(key))

    
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
    
    
_takeProfitOrderTickets = {}

def setTakeProfitOrderTicket(key, value):
    _takeProfitOrderTickets[str(key)] = value
    
def getTakeProfitOrderTicket(key):
    return _takeProfitOrderTickets.get(str(key))
    
def removeTakeProfitOrderTicket(key):
     _takeProfitOrderTickets.pop(key, None)
    
    
_highestPrice = {}

def setHighestPrice(key, value):
    _highestPrice[str(key)] = value
    
def getHighestPrice(key):
    return _highestPrice.get(str(key))
    
def removeHighestPrice(key):
    _highestPrice.pop(key, None)
    
    
_trailingStopTickets = {}

def setTrailingStopOrderTicket(key, value):
    _trailingStopTickets[str(key)] = value
    
def getTrailingStopOrderTicket(key):
    return _trailingStopTickets.get(str(key))
    
def removeTrailingStopOrderTicket(key):
     _trailingStopTickets.pop(key, None)
     
_stoppedOutSymbols = set()

def addStoppedOutSymbol(symbol):
    _stoppedOutSymbols.add(str(symbol))
    
def getStoppedOutSymbols():
    return _stoppedOutSymbols
    
def removeStoppedOutSymbol(symbol):
    _stoppedOutSymbols.remove(str(symbol))
    
def isStoppedOutSymbol(symbol):
    return str(symbol) in _stoppedOutSymbols
