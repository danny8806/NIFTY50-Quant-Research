# NIFTY50 Quant Research

Institutional-grade quantitative research framework for the Indian equity market. Downloads historical data for top NIFTY50 stocks, backtests multiple trading strategies, and generates comprehensive performance analytics and reports.

## Key Findings

**Benchmark (NIFTY50):** 2007–2026 | CAGR: **9.61%** | Volatility: **20.66%** | Sharpe: **0.3056** | Max DD: **-59.86%**

| Finding | Detail |
|---------|--------|
| Best Stock CAGR | ASIANPAINT (**21.21%**) |
| Worst Stock CAGR | BHARTIARTL (**9.85%**) |
| Stocks beating benchmark | **15/15** (all 15 stocks outpaced NIFTY50 in CAGR) |
| Volatility vs benchmark | **0/15** stocks have lower volatility than NIFTY50 |
| Alpha range | **+2.91%** (RELIANCE) to **+14.77%** (ASIANPAINT) — all positive |
| Best strategy (avg CAGR) | **MACD** (3.76%) |
| Best strategy (avg Sharpe) | **MACD** (0.2522) |
| Best single result | MACD on INFY: **328.86%** return, **5.53%** CAGR |

**Strategy Averages (across RELIANCE, TCS, INFY):**

| Strategy | Avg Return | Avg CAGR | Avg Sharpe |
|----------|-----------|---------|-----------|
| EMA Crossover | 101.12% | 2.02% | 0.1298 |
| RSI | 182.17% | 3.62% | 0.2340 |
| **MACD** | **198.67%** | **3.76%** | **0.2522** |
| Bollinger Bands | 103.10% | 2.18% | 0.1413 |

## Features

- **4 Trading Strategies**: EMA Crossover, RSI, MACD, Bollinger Bands
- **15 NIFTY50 Stocks**: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, BHARTIARTL, HINDUNILVR, ITC, LT, AXISBANK, KOTAKBANK, ASIANPAINT, MARUTI, SUNPHARMA
- **NIFTY50 Benchmark** comparison (^NSEI)
- **Risk Analytics**: CAGR, Sharpe Ratio, Volatility, Max Drawdown, Alpha, Beta
- **Performance Reports**: JSON, TXT, PDF, and interactive HTML formats
- **Streamlit Dashboard** for live exploration
- **18 years of data** (2007–2026) from Yahoo Finance — all metrics computed over the **same time period**

## Quick Start

```bash
pip install -r requirements.txt
python main.py              # Download data (15 stocks + NIFTY50 benchmark)
python run_analysis.py      # Run backtests + generate JSON results
python generate_combined_html.py  # Generate interactive HTML report
python generate_report.py         # Generate PDF report
open reports/combined_report.html # View report
```

## Reports

| Report | Path | Description |
|--------|------|-------------|
| Interactive HTML | `reports/combined_report.html` | Full analysis with Plotly charts, tables, conclusions |
| PDF Report | `reports/quant_research_report.pdf` | Print-friendly PDF with all results |
| Backtest JSON | `reports/backtest_results.json` | Structured metrics for programmatic access |
| Benchmark Comparison CSV | `reports/benchmark_reports/benchmark_comparison.csv` | 15 stocks vs NIFTY50 across all metrics |
| Benchmark Comparison TXT | `reports/benchmark_reports/benchmark_comparison.txt` | Human-readable benchmark comparison |
| Comprehensive Results | `reports/portfolio_reports/comprehensive_results.txt` | Per-stock detail, rankings, strategy averages |

## Screenshots

![Project Overview & Benchmark](Screenshots/Screenshot%202026-05-22%20at%202.10.20%E2%80%AFPM.png)
![Stock Performance Table](Screenshots/Screenshot%202026-05-22%20at%202.10.23%E2%80%AFPM.png)
![Benchmark vs Stocks Comparison](Screenshots/Screenshot%202026-05-22%20at%202.10.28%E2%80%AFPM.png)
![Strategy Backtest Results](Screenshots/Screenshot%202026-05-22%20at%202.10.31%E2%80%AFPM.png)
![Strategy Averages Chart](Screenshots/Screenshot%202026-05-22%20at%202.10.34%E2%80%AFPM.png)
![Sharpe Ratio Heatmap](Screenshots/Screenshot%202026-05-22%20at%202.10.37%E2%80%AFPM.png)
![Return Comparison Chart](Screenshots/Screenshot%202026-05-22%20at%202.10.39%E2%80%AFPM.png)
![Equity Curves (1)](Screenshots/Screenshot%202026-05-22%20at%202.10.41%E2%80%AFPM.png)
![Equity Curves (2)](Screenshots/Screenshot%202026-05-22%20at%202.10.45%E2%80%AFPM.png)
![Conclusions](Screenshots/Screenshot%202026-05-22%20at%202.10.50%E2%80%AFPM.png)
![Recommendations](Screenshots/Screenshot%202026-05-22%20at%202.10.59%E2%80%AFPM.png)
![Full Report View](Screenshots/Screenshot%202026-05-22%20at%202.11.04%E2%80%AFPM.png)

## Project Structure

```
├── config/settings.py        # Stock list, benchmark, date range
├── utils/
│   ├── data_loader.py        # yfinance download & load
│   └── indicators.py         # EMA, SMA, RSI indicators
├── strategies/
│   ├── ema_crossover.py      # EMA 20/50 crossover
│   ├── rsi_strategy.py       # RSI 14 oversold/overbought
│   ├── macd_strategy.py      # MACD 12/26
│   └── bollinger_strategy.py # Bollinger Bands 20,2
├── analytics/
│   ├── returns_analysis.py   # CAGR, daily/log returns
│   ├── risk_analysis.py      # Volatility, Sharpe, Max DD
│   ├── benchmark_analysis.py # Alpha, Beta
│   └── visualization.py      # Equity curve plotting
├── data/
│   ├── raw/                  # Stock OHLCV data
│   ├── benchmark/            # NIFTY50 index data
│   └── processed/
├── reports/
│   ├── combined_report.html  # Interactive HTML analysis
│   ├── quant_research_report.pdf  # Full PDF report
│   ├── backtest_results.json  # Structured metrics
│   ├── stock_reports/        # Per-stock detail
│   ├── strategy_reports/     # Per-strategy detail
│   ├── benchmark_reports/    # NIFTY50 analysis
│   └── portfolio_reports/    # Portfolio summary
├── images/                   # Backtest chart HTMLs
├── dashboard/app.py          # Streamlit app
└── main.py                   # Entry point
```

## Dependencies

pandas, numpy, yfinance, backtesting.py, plotly, streamlit, scipy, statsmodels, quantstats, vectorbt, fpdf2

## Disclaimer

**This project is for educational and research purposes only.**

The content, analysis, and reports generated by this framework are provided solely for informational and academic use. They do not constitute financial advice, investment recommendations, or solicitation to buy or sell any securities.

- Past performance is not indicative of future results.
- Backtested results are hypothetical and may differ materially from actual trading outcomes due to factors such as market liquidity, slippage, transaction costs, and execution timing.
- The trading strategies implemented here are simplified versions and should not be used for live trading without thorough validation and risk assessment.
- Always consult a qualified financial advisor before making investment decisions.

**No warranty** is provided, express or implied, regarding the accuracy, completeness, or fitness for a particular purpose of the data, analysis, or reports generated by this framework.
