
import pandas as pd
from backtesting import Strategy

class BollingerStrategy(Strategy):

    def init(self):
        close = pd.Series(self.data.Close.s)

        self.sma = self.I(lambda: close.rolling(20).mean().values)
        self.std = self.I(lambda: close.rolling(20).std().values)

    def next(self):
        upper = self.sma[-1] + 2 * self.std[-1]
        lower = self.sma[-1] - 2 * self.std[-1]

        if self.data.Close[-1] < lower:
            self.buy()

        elif self.data.Close[-1] > upper:
            self.position.close()
