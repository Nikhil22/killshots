from KSUniverseModel import KSUniverseModel
import SharedState
import MarketStructure

class Killshots(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 2, 1)
        self.SetEndDate(2020, 2, 28)
        self.SetCash(24000) 
        self.AddUniverseSelection(KSUniverseModel())
        self.UniverseSettings.Resolution = Resolution.Minute
        self.riskPerTrade = 0.005
        self.minCash = self.Portfolio.Cash / 2
        self.DefaultOrderProperties.TimeInForce = TimeInForce.Day
        
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
            self.LimitOrder(symbol, quantity, entryPrice)
            SharedState.addToSymbolsWithOpenOrders(symbol)

        # Take profit, stop loss
        for kvp in self.Securities:
            symbol = kvp.Key
            security = kvp.Value

            if security.Holdings.IsLong:
                high = security.High
                close = security.Close
                low = security.Low
                if high >= SharedState.getTakeProfitPrice(symbol):
                    self.Liquidate(symbol)
                    continue
                if close <= SharedState.getStopLossPrice(symbol):
                    self.Liquidate(symbol)
