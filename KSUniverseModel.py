from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel
from SymbolData import SymbolData
import SharedState
import MarketStructure

class KSUniverseModel(FundamentalUniverseSelectionModel):
    def __init__(self, filterFineData = True, universeSettings = None):
        super().__init__(filterFineData, universeSettings)
        
    def SelectCoarse(self, algorithm, coarse):
        MIN_VOLUME = 1e6
        
        return [
            x.Symbol for x in coarse if (
                x.HasFundamentalData
                and x.Volume > MIN_VOLUME
                and self.NotInvested(algorithm, x.Symbol)
            )
            # x.Symbol for x in coarse if (
            #     "TBLT" in str(x.Symbol)
            #     and self.NotInvested(algorithm, x.Symbol)
            # )
        ]
        
    def SelectFine(self, algorithm, fine):
        MAX_SHARE_COUNT = 50e6
        MAX_BARS_BACK = 200
        LENGTH_OF_BOTTOM = 30
        initialFilter = [
            x.Symbol for x in fine if (
                x.CompanyProfile.SharesOutstanding <= MAX_SHARE_COUNT
                # no shell companies
                and x.AssetClassification.MorningstarIndustryCode != 10350010
            )
        ]
        
        historySlices = algorithm.History(initialFilter, MAX_BARS_BACK, Resolution.Daily)
        for symbol, history in historySlices.groupby(level=0):
            SharedState.updateHistory(symbol, history)
            
        def isBottom(x):
            symbol = x
            history = SharedState.getHistory(symbol)
            if history is None:
                return False
            closingPrices = history["close"][-LENGTH_OF_BOTTOM:].tolist()
            bottom = MarketStructure.advancedDoubleBottom(closingPrices, symbol)
            if bottom["state"] is True:
                SharedState.updateStopLossPrice(symbol, bottom['laggingBottomPrice'])
                SharedState.updateEntryPrice(
                    symbol, bottom["midPointPrice"]
                )
                SharedState.updateTakeProfitPrice(symbol, [bottom["midPointPrice"], bottom['laggingBottomPrice']], 2)
                return True
            return False
            
        hasBottom = list(filter(isBottom, initialFilter))
        
        finalSymbols = [x for x in hasBottom]
        
        return finalSymbols
        
    def NotInvested(self, algorithm, symbol):
        return not (
                        symbol in algorithm.Securities 
                        and algorithm.Securities[symbol].Invested
                    )
