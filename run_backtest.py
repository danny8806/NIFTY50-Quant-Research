
from backtesting import Backtest
from utils.data_loader import load_data
from strategies.ema_crossover import EMACrossover
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.bollinger_strategy import BollingerStrategy

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]

strategies = {
    "EMA": EMACrossover,
    "RSI": RSIStrategy,
    "MACD": MACDStrategy,
    "BOLLINGER": BollingerStrategy
}

for stock in stocks:
    print(f"Running backtest for {stock}")

    df = load_data(f"data/raw/{stock}.csv")

    for name, strategy in strategies.items():

        bt = Backtest(
            df,
            strategy,
            cash=100000,
            commission=0.002
        )

        stats = bt.run()

        print("=" * 50)
        print(stock)
        print(name)
        print(stats)

        bt.plot()
