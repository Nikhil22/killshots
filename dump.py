# # If current price moved way up beyond open order(s), cancel open order(s)     
# allOpenOrders = SharedState.getSymbolsWithOpenOrders()
# for symbol in allOpenOrders:
#     openOrders = self.Transactions.GetOpenOrders(symbol)
#     if len(openOrders) == 0:
#         continue
#     latestOpenOrder = openOrders[-1].LimitPrice
#     currentPrice = self.Securities[symbol].Price
#     if (
#         currentPrice > latestOpenOrder 
#         and latestOpenOrder / currentPrice < MarketStructure.doubleBottomParameters["breakoutHeightThreshold"]
#         ):
#         #cancel all orders
#         self.Transactions.CancelOpenOrders(symbol)

# # Sell half
# quantity = self.Portfolio[symbol].Quantity
# quantityToSell = math.floor(quantity / 2) * -1
# self.MarketOrder(symbol, quantityToSell)

# #Create trailing stop
# self.StopMarketOrder(symbol, quantityToSell, 0.85 * close)
                    
# for symbol, history in historySlices.groupby(level=0):
#     if symbol not in self.averages:
#         self.averages[symbol] = SymbolData(symbol, history)
#     else:
#         avg = self.averages[symbol]
#         latestTime = history.loc[symbol].index[-1]
#         lastClose = history.loc[symbol].close.iloc[-1]
#         lastVolume = history.loc[symbol].volume.iloc[-1]
#         avg.updatePriceAvgs(latestTime, lastClose)
#         # avg.updateVolumeAvgs(latestTime, lastVolume)

#     SharedState.updateHistory(symbol, history)

# def passesAverages(x):
#     return (
#         x.isUptrend() 
#         # and x.hasSufficientVolume(MIN_VOLUME)
#     )
# initialFilter2 = list(filter(lambda x: passesAverages(x), self.averages.values()))
