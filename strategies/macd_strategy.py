
import pandas as pd
from backtesting import Strategy

class MACDStrategy(Strategy):

    def init(self):
        close = pd.Series(self.data.Close.s)

        self.ema12 = self.I(lambda: close.ewm(span=12).mean().values)
        self.ema26 = self.I(lambda: close.ewm(span=26).mean().values)

    def next(self):
        macd = self.ema12[-1] - self.ema26[-1]

        if macd > 0:
            self.buy()

        elif macd < 0:
            self.position.close()
