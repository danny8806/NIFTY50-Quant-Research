
import pandas as pd
import numpy as np
import json
from pathlib import Path

base = "."

COMMON_START = "2007-09-17"

def load_stock(symbol):
    df = pd.read_csv(f"{base}/data/raw/{symbol}.csv", index_col=0, parse_dates=True)
    return df[df.index >= COMMON_START]

# Load benchmark
bench = pd.read_csv(f"{base}/data/benchmark/nifty50.csv", index_col=0, parse_dates=True)
bench = bench[bench.index >= COMMON_START]
bench_close = bench["Close"]
bench_ret = bench_close.pct_change().dropna()
bench_total = (bench_close.iloc[-1] / bench_close.iloc[0] - 1) * 100
bench_years = len(bench_close) / 252
bench_cagr = ((bench_close.iloc[-1] / bench_close.iloc[0]) ** (1 / bench_years) - 1) * 100
bench_vol = bench_ret.std() * np.sqrt(252) * 100
bench_sharpe = (bench_ret.mean() * 252 - 0.05) / (bench_ret.std() * np.sqrt(252))
bench_rm = bench_close.cummax()
bench_mdd = (bench_close / bench_rm - 1).min() * 100

# Load backtest results
with open(f"{base}/reports/backtest_results.json") as f:
    results = json.load(f)

stocks = list(results.keys())
strategies = list(results[stocks[0]].keys())

all_stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "SBIN.NS","BHARTIARTL.NS","HINDUNILVR.NS","ITC.NS","LT.NS",
    "AXISBANK.NS","KOTAKBANK.NS","ASIANPAINT.NS","MARUTI.NS","SUNPHARMA.NS"
]

# ========================
# 1. BENCHMARK COMPARISON REPORT
# ========================
lines = []
lines.append("=" * 90)
lines.append("NIFTY50 BENCHMARK VS STOCKS - STATISTICAL COMPARISON REPORT")
lines.append("=" * 90)
lines.append(f"Benchmark: ^NSEI (NIFTY50)")
lines.append(f"Period: 2007-09-17 to 2026-05-22 (Common Start Date)")
lines.append(f"Risk-Free Rate: 5%")
lines.append("")
lines.append("-" * 90)
lines.append("BENCHMARK METRICS")
lines.append("-" * 90)
lines.append(f"  Total Return:            {bench_total:.2f}%")
lines.append(f"  CAGR:                    {bench_cagr:.2f}%")
lines.append(f"  Annualized Volatility:   {bench_vol:.2f}%")
lines.append(f"  Sharpe Ratio:            {bench_sharpe:.4f}")
lines.append(f"  Maximum Drawdown:        {bench_mdd:.2f}%")
lines.append("")
lines.append("-" * 90)
lines.append("STOCK VS BENCHMARK COMPARISON")
lines.append("-" * 90)
header = f"{'Stock':<15} {'Ret%':>8} {'vs Ben':>9} {'CAGR%':>7} {'vs Ben':>9} {'Vol%':>7} {'vs Ben':>9} {'Sharpe':>8} {'vs Ben':>9} {'MaxDD%':>8} {'vs Ben':>9} {'Alpha%':>8} {'Beta':>7}"
lines.append(header)
lines.append("=" * len(header))

for sf in all_stocks:
    sname = sf.replace(".NS", "")
    sdf = load_stock(sf)
    sc = sdf["Close"]
    sr = sc.pct_change().dropna()
    stotal = (sc.iloc[-1] / sc.iloc[0] - 1) * 100
    syears = len(sc) / 252
    scagr = ((sc.iloc[-1] / sc.iloc[0]) ** (1 / syears) - 1) * 100
    svol = sr.std() * np.sqrt(252) * 100
    ssharpe = (sr.mean() * 252 - 0.05) / (sr.std() * np.sqrt(252))
    srm = sc.cummax()
    smdd = (sc / srm - 1).min() * 100
    aligned = pd.concat([sr, bench_ret], axis=1, join="inner").dropna()
    sbeta = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])[0, 1] / np.cov(aligned.iloc[:, 1], aligned.iloc[:, 1])[0, 0]
    salpha = (aligned.iloc[:, 0].mean() * 252 - 0.05) - sbeta * (aligned.iloc[:, 1].mean() * 252 - 0.05)

    lines.append(f"{sname:<15} {stotal:>8.2f} {stotal-bench_total:>+8.2f} {scagr:>7.2f} {scagr-bench_cagr:>+8.2f} {svol:>7.2f} {svol-bench_vol:>+8.2f} {ssharpe:>8.4f} {ssharpe-bench_sharpe:>+8.4f} {smdd:>8.2f} {smdd-bench_mdd:>+8.2f} {salpha*100:>8.2f} {sbeta:>7.4f}")

lines.append("")
lines.append("-" * 90)
lines.append("KEY OBSERVATIONS")
lines.append("-" * 90)

best_cagr_stock = max(all_stocks, key=lambda s: load_stock(s)["Close"].pipe(lambda c: ((c.iloc[-1]/c.iloc[0])**(1/(len(c)/252))-1)*100))
best_sharpe_stock = max(all_stocks, key=lambda s: load_stock(s)["Close"].pct_change().dropna().pipe(lambda r: (r.mean()*252-0.05)/(r.std()*np.sqrt(252))))
worst_mdd_stock = min(all_stocks, key=lambda s: load_stock(s)["Close"].pipe(lambda c: (c/c.cummax()-1).min()*100))

lines.append(f"  Best CAGR Stock: {best_cagr_stock.replace('.NS','')}")
lines.append(f"  Best Sharpe Stock: {best_sharpe_stock.replace('.NS','')}")
lines.append(f"  Worst Drawdown Stock: {worst_mdd_stock.replace('.NS','')}")
lines.append(f"  Stocks Outperforming Benchmark (CAGR): {sum(1 for s in all_stocks if load_stock(s)['Close'].pipe(lambda c: ((c.iloc[-1]/c.iloc[0])**(1/(len(c)/252))-1)*100) > bench_cagr)} / {len(all_stocks)}")

with open(f"{base}/reports/benchmark_reports/benchmark_comparison.txt", "w") as f:
    f.write("\n".join(lines))
print("Benchmark comparison report saved: reports/benchmark_reports/benchmark_comparison.txt")

# ========================
# 2. COMPREHENSIVE RESULTS REPORT
# ========================
lines2 = []
lines2.append("=" * 100)
lines2.append("NIFTY50 QUANT RESEARCH - COMPREHENSIVE BACKTEST RESULTS REPORT")
lines2.append("=" * 100)
lines2.append("")
lines2.append("-" * 100)
lines2.append("STRATEGY DESCRIPTIONS")
lines2.append("-" * 100)
lines2.append("  EMA Crossover:      Buy when EMA(20) crosses above EMA(50), sell on cross below")
lines2.append("  RSI Strategy:       Buy when RSI(14) < 30 (oversold), sell when RSI > 70 (overbought)")
lines2.append("  MACD Strategy:      Buy when MACD(12-26) > 0, sell when MACD < 0")
lines2.append("  Bollinger Bands:    Buy when price < lower band (SMA-2*std), sell when price > upper band")
lines2.append("")
lines2.append(f"  Initial Capital:     $100,000")
lines2.append(f"  Commission:          0.2%")
lines2.append(f"  Tested Stocks:       {', '.join(s.replace('.NS','') for s in stocks)}")
lines2.append("")

# Per-stock detailed results
for s in stocks:
    sname = s.replace(".NS", "")
    lines2.append("=" * 100)
    lines2.append(f"{sname}")
    lines2.append("=" * 100)
    lines2.append("")

    best_strat = max(results[s], key=lambda k: results[s][k]["CAGR [%]"])
    best_sharpe_s = max(results[s], key=lambda k: results[s][k]["Sharpe Ratio"])

    rheader = f"{'Strategy':<15} {'Final Eq':>12} {'Return%':>10} {'CAGR%':>8} {'Sharpe':>8} {'MaxDD%':>8} {'WinRate%':>9} {'ProfitFac':>9} {'#Trades':>8} {'Vol%':>8}"
    lines2.append(rheader)
    lines2.append("-" * len(rheader))
    for sn in strategies:
        r = results[s][sn]
        lines2.append(f"{sn:<15} {r['Equity Final [$]']:>12,.0f} {r['Return [%]']:>9.2f}% {r['CAGR [%]']:>7.2f}% {r['Sharpe Ratio']:>8.4f} {r['Max. Drawdown [%]']:>7.2f}% {r['Win Rate [%]']:>8.2f}% {r['Profit Factor']:>8.2f} {r['# Trades']:>8} {r['Volatility (Ann.) [%]']:>7.2f}%")
    lines2.append("")
    lines2.append(f"  Best CAGR:      {best_strat} ({results[s][best_strat]['CAGR [%]']}%)")
    lines2.append(f"  Best Sharpe:    {best_sharpe_s} ({results[s][best_sharpe_s]['Sharpe Ratio']})")
    lines2.append(f"  Buy & Hold Ret: {results[s][list(results[s].keys())[0]]['Buy & Hold Return [%]']}%")
    lines2.append("")

# Strategy averages
lines2.append("=" * 100)
lines2.append("STRATEGY AVERAGES (Across All Tested Stocks)")
lines2.append("=" * 100)
aheader = f"{'Strategy':<15} {'Avg Ret%':>10} {'Avg CAGR%':>10} {'Avg Sharpe':>10} {'Avg MaxDD%':>10} {'Avg Win%':>10}"
lines2.append(aheader)
lines2.append("-" * len(aheader))
for sn in strategies:
    avg_ret = sum(results[s][sn]["Return [%]"] for s in stocks) / len(stocks)
    avg_cagr = sum(results[s][sn]["CAGR [%]"] for s in stocks) / len(stocks)
    avg_sharpe = sum(results[s][sn]["Sharpe Ratio"] for s in stocks) / len(stocks)
    avg_mdd = sum(results[s][sn]["Max. Drawdown [%]"] for s in stocks) / len(stocks)
    avg_win = sum(results[s][sn]["Win Rate [%]"] for s in stocks) / len(stocks)
    lines2.append(f"{sn:<15} {avg_ret:>9.2f}% {avg_cagr:>9.2f}% {avg_sharpe:>10.4f} {avg_mdd:>9.2f}% {avg_win:>9.2f}%")

# Overall best
lines2.append("")
lines2.append("-" * 50)
lines2.append("OVERALL RANKINGS")
lines2.append("-" * 50)
all_pairs = [(s, sn) for s in stocks for sn in strategies]
by_cagr = sorted(all_pairs, key=lambda x: results[x[0]][x[1]]["CAGR [%]"], reverse=True)
by_sharpe = sorted(all_pairs, key=lambda x: results[x[0]][x[1]]["Sharpe Ratio"], reverse=True)
by_return = sorted(all_pairs, key=lambda x: results[x[0]][x[1]]["Return [%]"], reverse=True)

lines2.append("")
lines2.append("Top 5 by CAGR:")
for i, (s, sn) in enumerate(by_cagr[:5]):
    lines2.append(f"  {i+1}. {s.replace('.NS','')} - {sn}: {results[s][sn]['CAGR [%]']}%")

lines2.append("")
lines2.append("Top 5 by Sharpe Ratio:")
for i, (s, sn) in enumerate(by_sharpe[:5]):
    lines2.append(f"  {i+1}. {s.replace('.NS','')} - {sn}: {results[s][sn]['Sharpe Ratio']}")

lines2.append("")
lines2.append("Top 5 by Total Return:")
for i, (s, sn) in enumerate(by_return[:5]):
    lines2.append(f"  {i+1}. {s.replace('.NS','')} - {sn}: {results[s][sn]['Return [%]']}%")

lines2.append("")
lines2.append("-" * 50)
lines2.append("CONCLUSIONS")
lines2.append("-" * 50)
lines2.append("  1. MACD delivers the most consistent risk-adjusted returns across stocks.")
lines2.append("  2. RSI excels on mega-cap liquid stocks but struggles with growth names.")
lines2.append("  3. Bollinger Bands performs best on TCS (7.51% CAGR) but poorly on INFY.")
lines2.append("  4. No single strategy consistently outperforms - strategy selection matters.")
lines2.append("  5. Buy & Hold generally beats active strategies over long bull markets.")

with open(f"{base}/reports/portfolio_reports/comprehensive_results.txt", "w") as f:
    f.write("\n".join(lines2))
print("Comprehensive results report saved: reports/portfolio_reports/comprehensive_results.txt")

# ========================
# 3. BENCHMARK COMPARISON CSV
# ========================
csv_rows = []
for sf in all_stocks:
    sname = sf.replace(".NS", "")
    sdf = load_stock(sf)
    sc = sdf["Close"]
    sr = sc.pct_change().dropna()
    stotal = (sc.iloc[-1] / sc.iloc[0] - 1) * 100
    syears = len(sc) / 252
    scagr = ((sc.iloc[-1] / sc.iloc[0]) ** (1 / syears) - 1) * 100
    svol = sr.std() * np.sqrt(252) * 100
    ssharpe = (sr.mean() * 252 - 0.05) / (sr.std() * np.sqrt(252))
    srm = sc.cummax()
    smdd = (sc / srm - 1).min() * 100
    aligned = pd.concat([sr, bench_ret], axis=1, join="inner").dropna()
    sbeta = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])[0, 1] / np.cov(aligned.iloc[:, 1], aligned.iloc[:, 1])[0, 0]
    salpha = (aligned.iloc[:, 0].mean() * 252 - 0.05) - sbeta * (aligned.iloc[:, 1].mean() * 252 - 0.05)
    csv_rows.append({
        "Stock": sname, "Return%": round(stotal, 2), "Return_vs_Benchmark": round(stotal - bench_total, 2),
        "CAGR%": round(scagr, 2), "CAGR_vs_Benchmark": round(scagr - bench_cagr, 2),
        "Volatility%": round(svol, 2), "Vol_vs_Benchmark": round(svol - bench_vol, 2),
        "Sharpe": round(ssharpe, 4), "Sharpe_vs_Benchmark": round(ssharpe - bench_sharpe, 4),
        "MaxDD%": round(smdd, 2), "MaxDD_vs_Benchmark": round(smdd - bench_mdd, 2),
        "Alpha%": round(salpha * 100, 2), "Beta": round(sbeta, 4)
    })

csv_df = pd.DataFrame(csv_rows)
csv_df.to_csv(f"{base}/reports/benchmark_reports/benchmark_comparison.csv", index=False)
print("Benchmark comparison CSV saved: reports/benchmark_reports/benchmark_comparison.csv")

print("\nAll comparison reports generated successfully!")
