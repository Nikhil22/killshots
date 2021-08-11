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
