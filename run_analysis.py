
import json
from backtesting import Backtest
from utils.data_loader import load_data
from strategies.ema_crossover import EMACrossover
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.bollinger_strategy import BollingerStrategy

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

strategies = {
    "EMA": EMACrossover,
    "RSI": RSIStrategy,
    "MACD": MACDStrategy,
    "BOLLINGER": BollingerStrategy
}

results = {}

for stock in stocks:
    results[stock] = {}
    df = load_data(f"data/raw/{stock}.csv")
    for name, strategy in strategies.items():
        bt = Backtest(df, strategy, cash=100000, commission=0.002)
        stats = bt.run()
        results[stock][name] = {
            "Equity Final [$]": round(stats["Equity Final [$]"], 2),
            "Return [%]": round(stats["Return [%]"], 2),
            "CAGR [%]": round(stats["CAGR [%]"], 2),
            "Sharpe Ratio": round(stats["Sharpe Ratio"], 4),
            "Max. Drawdown [%]": round(stats["Max. Drawdown [%]"], 2),
            "Buy & Hold Return [%]": round(stats["Buy & Hold Return [%]"], 2),
            "# Trades": int(stats["# Trades"]),
            "Win Rate [%]": round(stats["Win Rate [%]"], 2),
            "Profit Factor": round(stats["Profit Factor"], 4),
            "Volatility (Ann.) [%]": round(stats["Volatility (Ann.) [%]"], 2),
            "Alpha [%]": round(stats["Alpha [%]"], 2),
            "Beta": round(stats["Beta"], 4),
        }

with open("reports/backtest_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary table
print(f"{'Stock':<15} {'Strategy':<10} {'Final Equity':<15} {'Return%':<10} {'CAGR%':<8} {'Sharpe':<8} {'MaxDD%':<8} {'WinRate%':<8} {'ProfitFact':<10}")
print("=" * 100)
for stock in stocks:
    for name in strategies:
        r = results[stock][name]
        print(f"{stock:<15} {name:<10} {r['Equity Final [$]']:<15} {r['Return [%]']:<10} {r['CAGR [%]']:<8} {r['Sharpe Ratio']:<8} {r['Max. Drawdown [%]']:<8} {r['Win Rate [%]']:<8} {r['Profit Factor']:<10}")
    print()
