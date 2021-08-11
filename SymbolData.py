class SymbolData(object):
    def __init__(self, symbol, history):
        self.symbol = symbol
        self.longTerm = ExponentialMovingAverage(200)
        self.mediumTerm = ExponentialMovingAverage(100)
        self.shortTerm = ExponentialMovingAverage(50)
        self.superShortTerm = ExponentialMovingAverage(30)
        self.historicalVolume = SimpleMovingAverage(30)
        
        history.loc[self.symbol].apply(lambda row: self.updatePriceAvgs(row.name, row.close), axis=1)
        # history.loc[self.symbol].apply(lambda row: self.updateVolumeAvgs(row.name, row.volume), axis=1)

    def updatePriceAvgs(self, time, value):
        self.longTerm.Update(time, value)
        self.mediumTerm.Update(time, value)
        self.shortTerm.Update(time, value)
        self.superShortTerm.Update(time, value)
        self.historicalVolume.Update(time, value)
        
    def updateVolumeAvgs(self, time, value):
        self.historicalVolume.Update(time, value)
    
    def isUptrend(self):
        longTerm = self.longTerm.Current.Value
        mediumTerm = self.mediumTerm.Current.Value
        shortTerm = self.shortTerm.Current.Value
        superShortTerm = self.superShortTerm.Current.Value
        
        return (
            mediumTerm > longTerm
            and shortTerm > mediumTerm
            and superShortTerm > shortTerm
        )
        
    def hasSufficientVolume(self, threshold):
        return (
            self.historicalVolume.Current.Value > threshold
        )
