from KSUniverseModel import KSUniverseModel
import SharedState
import math

class Killshots(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2015, 12, 31)
        self.SetCash(24000) 
        self.AddUniverseSelection(KSUniverseModel())
        self.UniverseSettings.Resolution = Resolution.Minute
        self.riskPerTrade = 0.005
        self.minCash = self.Portfolio.Cash / 2

    def OnData(self, slice):
        for key in slice.Bars:
            symbol = key.Value.Symbol
            currentPrice = slice.Bars[symbol].Close
            entryPrice = SharedState.getEntryPrice(symbol)
            stopLossPrice = SharedState.getStopLossPrice(symbol)
            quantity = SharedState.calculateQuantity(
                entryPrice, stopLossPrice, self.Portfolio.TotalPortfolioValue * self.riskPerTrade
            )
            if currentPrice <= stopLossPrice:
                continue
            if self.Portfolio.Cash - (entryPrice * quantity) <= self.minCash:
                continue
            if len(self.Transactions.GetOpenOrders(symbol)) > 0:
                continue
            if self.Securities[symbol].Invested:
                continue
            if currentPrice > entryPrice:
                continue
            if SharedState.isStoppedOutSymbol(symbol):
                continue
            self.MarketOrder(symbol, quantity)
            holdings = self.Portfolio[symbol].Quantity
            quantityToSell = math.floor(holdings/2)
            orderTicket = self.LimitOrder(symbol, -quantityToSell, SharedState.getTakeProfitPrice(symbol))
            SharedState.setTakeProfitOrderTicket(symbol, orderTicket)

        # Take profit, stop loss
        for kvp in self.Securities:
            symbol = kvp.Key
            security = kvp.Value

            if security.Holdings.IsLong:
                high = security.High
                close = security.Close
                low = security.Low
                highestPrice = SharedState.getHighestPrice(symbol)
                
                if highestPrice is not None and close > SharedState.getHighestPrice(symbol):
                    SharedState.setHighestPrice(symbol, close)
                    updateFields = UpdateOrderFields()
                    updateFields.StopPrice = close * 0.9
                    trailingStopTicket = SharedState.getTrailingStopOrderTicket(symbol)
                    trailingStopTicket.Update(updateFields)
                
                if close <= SharedState.getStopLossPrice(symbol):
                    SharedState.addStoppedOutSymbol(symbol)
                    self.Liquidate(symbol)
                    
    def OnOrderEvent(self, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        symbol = order.Symbol
        takeProfitOrderTicket = SharedState.getTakeProfitOrderTicket(symbol)
        trailingStopOrderTicket = SharedState.getTrailingStopOrderTicket(symbol)
        
        if orderEvent.Status != OrderStatus.Filled:
            return
    
        if takeProfitOrderTicket is not None and order.Id == takeProfitOrderTicket.OrderId:
            holdings = self.Portfolio[symbol].Quantity
            fillPrice = orderEvent.FillPrice
            ticket = self.StopMarketOrder(symbol, -holdings, 0.8 * fillPrice)
            SharedState.setTrailingStopOrderTicket(symbol, ticket)
            SharedState.setHighestPrice(symbol, fillPrice)
            return
        
        if trailingStopOrderTicket is not None and order.Id == trailingStopOrderTicket.OrderId:
            SharedState.removeHighestPrice(symbol)
            SharedState.removeTrailingStopOrderTicket(symbol)
            SharedState.removeTakeProfitOrderTicket(symbol)
            
    def OnSecuritiesChanged(self, changes):
        for x in changes.RemovedSecurities:
            symbol = x.Symbol
            if SharedState.isStoppedOutSymbol(symbol):
                SharedState.removeStoppedOutSymbol(symbol)
