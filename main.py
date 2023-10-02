"""

Uses mean reversion

Use Vector BT if you dont want to use quantt connect
"""

# region imports
from AlgorithmImports import *
# endregion


class CrawlingBlueKitten(QCAlgorithm):

    # only runs at initilization
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        # SPY tracks S&P, idea of how stock market is doing
        # Resolution.Daily - checks market daily
        self.spy = self.AddEquity("SPY", Resolution.Daily).symbol
        self.SetBenchmark(self.spy)

        self.longSMA = self.SMA(self.spy, 100, Resolution.Daily)
        self.shortSMA = self.SMA(self.spy, 10, Resolution.Daily)

        self.Set(100, Resolution.Daily)

    def OnData(self, data: Slice):
        # algo build
        if data.ContainsKey(self.spy) and data[self.spy] is not None:
            price = data[self.spy].Value

            longSMA_Value = self.longSMA.Current.Value
            shortSMA_Value = self.longSMA.Current.Value

            if (not self.Portfolio[self.spy].Invested) and (shortSMA_Value > longSMA_Value):
                # 1 means spending entire portfolio, 0.5 = half
                self.SetHoldings(self.spy, 1)
            if (self.Portfolio[self.spy].Invested) and (shortSMA_Value < longSMA_Value):
                self.Liquidate(self.spy)
