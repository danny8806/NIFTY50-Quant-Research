
from backtesting import Strategy
from utils.indicators import ema

class EMACrossover(Strategy):

    fast = 20
    slow = 50

    def init(self):
        close = self.data.Close

        self.ema_fast = self.I(ema, close, self.fast)
        self.ema_slow = self.I(ema, close, self.slow)

    def next(self):
        if self.ema_fast[-1] > self.ema_slow[-1]:
            if not self.position:
                self.buy()

        elif self.ema_fast[-1] < self.ema_slow[-1]:
            if self.position:
                self.position.close()
