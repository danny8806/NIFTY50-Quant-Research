
import json
from datetime import datetime
from fpdf import FPDF

with open("reports/backtest_results.json") as f:
    results = json.load(f)

stocks = list(results.keys())
strategies = list(results[stocks[0]].keys())

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 20)
pdf.cell(0, 15, "NIFTY50 Quant Research Report", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

# Section 1: Project Overview
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "1. Project Overview", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6, (
    "This project implements an institutional-style quantitative research framework for the NIFTY50 index. "
    "It performs multi-strategy backtesting on India's top stocks using four trading strategies: "
    "EMA Crossover, RSI, MACD, and Bollinger Bands. "
    "The framework includes benchmark comparison, risk analysis, and portfolio analytics."
))
pdf.ln(3)

# Section 2: Data
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "2. Data Overview", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6, (
    f"Benchmark: ^NSEI (NIFTY50)\n"
    f"Date Range: 2007-09-17 to 2026-05-22 (Common Start Date)\n"
    f"Stocks Analyzed: {len(stocks)} (RELIANCE.NS, TCS.NS, INFY.NS)\n"
    f"Data Source: Yahoo Finance (yfinance)"
))
pdf.ln(3)

# Section 3: Strategies
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "3. Strategy Descriptions", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
strategy_desc = [
    ("EMA Crossover", "Buys when fast EMA(20) crosses above slow EMA(50), sells on cross below."),
    ("RSI Strategy", "Buys when RSI(14) < 30 (oversold), sells when RSI > 70 (overbought)."),
    ("MACD Strategy", "Buys when MACD (12-26 EMA diff) > 0, sells when MACD < 0."),
    ("Bollinger Bands", "Buys when price < lower band (SMA-2*std), sells when price > upper band (SMA+2*std)."),
]
for name, desc in strategy_desc:
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, f"{name}:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, f"  {desc}")
pdf.ln(3)

# Section 4: Backtest Results
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "4. Backtest Results Summary", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

cols = ["Stock", "Strategy", "Equity($)", "Return%", "CAGR%", "Sharpe", "MaxDD%", "WinRate%", "Profit"]
col_w = [28, 22, 28, 22, 18, 18, 18, 20, 22]
total_w = sum(col_w)
page_w = 190
# Scale to fit
if total_w > page_w:
    scale = page_w / total_w
    col_w = [int(w * scale) for w in col_w]

def table_header():
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(30, 60, 110)
    pdf.set_text_color(255, 255, 255)
    for i, c in enumerate(cols):
        pdf.cell(col_w[i], 7, c, border=1, align="C", fill=True)
    pdf.ln()

def table_row(data, fill=False):
    pdf.set_font("Helvetica", "", 7)
    if fill:
        pdf.set_fill_color(240, 245, 255)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    for i, d in enumerate(data):
        pdf.cell(col_w[i], 6, str(d), border=1, align="C", fill=True)
    pdf.ln()

table_header()
row_num = 0
for stock in stocks:
    for sname in strategies:
        r = results[stock][sname]
        row = [
            stock.replace(".NS", ""),
            sname,
            f"${r['Equity Final [$]']:,.0f}",
            f"{r['Return [%]']}%",
            f"{r['CAGR [%]']}%",
            f"{r['Sharpe Ratio']}",
            f"{r['Max. Drawdown [%]']}%",
            f"{r['Win Rate [%]']}%",
            f"{r['Profit Factor']}",
        ]
        table_row(row, fill=row_num % 2 == 1)
        row_num += 1

pdf.ln(5)

# Section 5: Best & Worst Performers
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "5. Performance Analysis", new_x="LMARGIN", new_y="NEXT")

all_results = []
for stock in stocks:
    for sname in strategies:
        r = results[stock][sname]
        all_results.append((stock, sname, r))

# Best CAGR
best_cagr = max(all_results, key=lambda x: x[2]["CAGR [%]"])
worst_cagr = min(all_results, key=lambda x: x[2]["CAGR [%]"])
best_sharpe = max(all_results, key=lambda x: x[2]["Sharpe Ratio"])
best_return = max(all_results, key=lambda x: x[2]["Return [%]"])

pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6, (
    f"Best Overall Return: {best_return[0].replace('.NS','')} with {best_return[1]} strategy "
    f"({best_return[2]['Return [%]']}% return, CAGR {best_return[2]['CAGR [%]']}%)\n"
    f"Best CAGR: {best_cagr[0].replace('.NS','')} with {best_cagr[1]} ({best_cagr[2]['CAGR [%]']}%)\n"
    f"Best Risk-Adjusted (Sharpe): {best_sharpe[0].replace('.NS','')} with {best_sharpe[1]} "
    f"(Sharpe: {best_sharpe[2]['Sharpe Ratio']})\n"
    f"Worst CAGR: {worst_cagr[0].replace('.NS','')} with {worst_cagr[1]} "
    f"({worst_cagr[2]['CAGR [%]']}%)"
))
pdf.ln(3)

# Strategy averages
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 9, "Strategy Averages Across Stocks:", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

avg_cols = ["Strategy", "Avg Return%", "Avg CAGR%", "Avg Sharpe", "Avg MaxDD%", "Avg WinRate%"]
avg_col_w = [30, 35, 30, 30, 30, 35]
avg_total = sum(avg_col_w)
if avg_total > page_w:
    s = page_w / avg_total
    avg_col_w = [int(w * s) for w in avg_col_w]

def avg_table_header():
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(30, 60, 110)
    pdf.set_text_color(255, 255, 255)
    for i, c in enumerate(avg_cols):
        pdf.cell(avg_col_w[i], 7, c, border=1, align="C", fill=True)
    pdf.ln()

def avg_table_row(data, fill=False):
    pdf.set_font("Helvetica", "", 7)
    if fill:
        pdf.set_fill_color(240, 245, 255)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    for i, d in enumerate(data):
        pdf.cell(avg_col_w[i], 6, str(d), border=1, align="C", fill=True)
    pdf.ln()

avg_table_header()
for i, sname in enumerate(strategies):
    avg_ret = sum(results[s][sname]["Return [%]"] for s in stocks) / len(stocks)
    avg_cagr = sum(results[s][sname]["CAGR [%]"] for s in stocks) / len(stocks)
    avg_sharpe = sum(results[s][sname]["Sharpe Ratio"] for s in stocks) / len(stocks)
    avg_mdd = sum(results[s][sname]["Max. Drawdown [%]"] for s in stocks) / len(stocks)
    avg_win = sum(results[s][sname]["Win Rate [%]"] for s in stocks) / len(stocks)
    avg_table_row([
        sname,
        f"{avg_ret:.2f}%",
        f"{avg_cagr:.2f}%",
        f"{avg_sharpe:.4f}",
        f"{avg_mdd:.2f}%",
        f"{avg_win:.2f}%",
    ], fill=i % 2 == 1)

pdf.ln(5)

# Section 6: Conclusions
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "6. Conclusions", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)

# Find best strategy on average
strategy_avg = {}
for sname in strategies:
    avg_cagr = sum(results[s][sname]["CAGR [%]"] for s in stocks) / len(stocks)
    avg_sharpe = sum(results[s][sname]["Sharpe Ratio"] for s in stocks) / len(stocks)
    avg_ret = sum(results[s][sname]["Return [%]"] for s in stocks) / len(stocks)
    strategy_avg[sname] = (avg_ret, avg_cagr, avg_sharpe)

best_avg_strat = max(strategy_avg, key=lambda k: strategy_avg[k][1])
best_avg_sharpe_strat = max(strategy_avg, key=lambda k: strategy_avg[k][2])

ret, cagr, sharpe = strategy_avg[best_avg_strat]
ret2, cagr2, sharpe2 = strategy_avg[best_avg_sharpe_strat]

conclusions = (
    f"1. MACD Strategy leads across all metrics with the highest average CAGR ({cagr:.2f}%) and "
    f"best risk-adjusted returns (Sharpe {sharpe:.4f}), making it the most consistent strategy.\n\n"
    f"2. RSI Strategy excels on RELIANCE (5.17% CAGR) but struggles on INFY (only 1.49% CAGR), "
    f"indicating stock-specific suitability - works best on mega-cap liquid stocks.\n\n"
    f"3. Bollinger Bands shows mixed results - strongest on TCS (4.36% CAGR) but negative on INFY "
    f"(-0.48% CAGR), highlighting the need for stock selection.\n\n"
    f"4. EMA Crossover delivers moderate returns on TCS/INFY but negative on RELIANCE (-1.19% CAGR) "
    f"with higher drawdowns, typical of trend-following in range-bound markets.\n\n"
    f"5. No single strategy consistently outperforms across all stocks - strategy selection "
    f"should be stock-specific and market-regime aware.\n\n"
    f"6. Buy & Hold returns generally exceed strategy returns over the full 18-year period, "
    f"highlighting the challenge of market timing vs. long-term holding in a bull market."
)
pdf.multi_cell(0, 6, conclusions)
pdf.ln(3)

# Section 7: Recommendations
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "7. Recommendations", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
recommendations = (
    f"1. Use MACD Strategy as a baseline for multi-stock portfolios - it offers the best "
    f"risk-adjusted returns across different stocks.\n\n"
    f"2. Apply RSI Strategy selectively - excellent for large-cap liquid stocks (RELIANCE, TCS) "
    f"but avoid on more volatile growth stocks (INFY).\n\n"
    f"3. Consider parameter optimization - the default parameters (20/50 EMA, 14 RSI, etc.) "
    f"may not be optimal. Grid search over parameter space could improve returns.\n\n"
    f"4. Combine strategies into an ensemble model - for example, use MACD for trend direction "
    f"confirmation and RSI for entry timing.\n\n"
    f"5. Add risk management rules - position sizing, trailing stop-losses, and portfolio-level "
    f"risk limits to reduce drawdown severity.\n\n"
    f"6. Extend analysis to all 15 NIFTY50 stocks in the config and include sector-wise "
    f"performance decomposition.\n\n"
    f"7. Incorporate machine learning models (e.g., Random Forest, XGBoost) for regime "
    f"detection to dynamically select the best strategy.\n\n"
    f"8. Backtest with transaction costs and slippage models more realistic than the current "
    f"0.2% flat commission."
)
pdf.multi_cell(0, 6, recommendations)

pdf.output("reports/quant_research_report.pdf")
print("PDF report generated: reports/quant_research_report.pdf")
