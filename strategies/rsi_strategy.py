
from backtesting import Strategy
from utils.indicators import rsi

class RSIStrategy(Strategy):

    def init(self):
        self.rsi_val = self.I(rsi, self.data.Close, 14)

    def next(self):
        if self.rsi_val[-1] < 30:
            self.buy()

        elif self.rsi_val[-1] > 70:
            self.position.close()
