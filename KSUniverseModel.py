from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel
from SymbolData import SymbolData
import SharedState
import MarketStructure

class KSUniverseModel(FundamentalUniverseSelectionModel):
    def __init__(self, filterFineData = True, universeSettings = None):
        super().__init__(filterFineData, universeSettings)
        self.averages = {}
        
    def SelectCoarse(self, algorithm, coarse):
        MIN_VOLUME = 300e3
        
        return [
            x.Symbol for x in coarse if (
                x.HasFundamentalData
                and x.Volume > MIN_VOLUME
                and self.NotInvested(algorithm, x.Symbol)
            )
            # x.Symbol for x in coarse if (
            #     "QDEL" in str(x.Symbol)
            #     and self.NotInvested(algorithm, x.Symbol)
            # )
        ]
        
    def SelectFine(self, algorithm, fine):
        MAX_SHARE_COUNT = 50e6
        MAX_BARS_BACK = 200
        LENGTH_OF_BOTTOM = 30
        MIN_VOLUME = 300e3
        
        initialFilter = [
            x.Symbol for x in fine if (
                x.CompanyProfile.SharesOutstanding <= MAX_SHARE_COUNT
                # no shell companies
                and x.AssetClassification.MorningstarIndustryCode != 10350010
                #div yield?
            )
        ]
        
        historySlices = algorithm.History(initialFilter, MAX_BARS_BACK, Resolution.Daily)
        for symbol, history in historySlices.groupby(level=0):
            if symbol not in self.averages:
                self.averages[symbol] = SymbolData(symbol, history)
            else:
                avg = self.averages[symbol]
                latestTime = history.loc[symbol].index[-1]
                lastClose = history.loc[symbol].close.iloc[-1]
                lastVolume = history.loc[symbol].volume.iloc[-1]
                avg.updatePriceAvgs(latestTime, lastClose)
                # avg.updateVolumeAvgs(latestTime, lastVolume)
            
            SharedState.updateHistory(symbol, history)
                
        def passesAverages(x):
            return (
                x.isUptrend() 
                # and x.hasSufficientVolume(MIN_VOLUME)
            )
        initialFilter2 = list(filter(lambda x: passesAverages(x), self.averages.values()))
        
        def isBottom(x):
            symbol = x.symbol
            closingPrices = SharedState.getHistory(symbol)["close"][-LENGTH_OF_BOTTOM:].tolist()
            bottom = MarketStructure.advancedDoubleBottom(closingPrices, symbol)
            if bottom["state"] is True:
                SharedState.updateStopLossPrice(symbol, bottom['laggingBottomPrice'])
                SharedState.updateEntryPrice(
                    symbol, bottom["midPointPrice"]
                )
                SharedState.updateTakeProfitPrice(symbol, [bottom["midPointPrice"], bottom['laggingBottomPrice']], 2)
                return True
            return False
            
        hasBottom = list(filter(isBottom, initialFilter2))
        
        finalSymbols = [x.symbol for x in hasBottom]
        
        return finalSymbols
        
    def NotInvested(self, algorithm, symbol):
        return not (
                        symbol in algorithm.Securities 
                        and algorithm.Securities[symbol].Invested
                    )
