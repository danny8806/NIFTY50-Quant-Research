# NIFTY50 Quant Research

Institutional-grade quantitative research framework for the Indian equity market. Downloads historical data for top NIFTY50 stocks, backtests multiple trading strategies, and generates comprehensive performance analytics and reports.

## Features

- **4 Trading Strategies**: EMA Crossover, RSI, MACD, Bollinger Bands
- **15 NIFTY50 Stocks**: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, BHARTIARTL, HINDUNILVR, ITC, LT, AXISBANK, KOTAKBANK, ASIANPAINT, MARUTI, SUNPHARMA
- **NIFTY50 Benchmark** comparison (^NSEI)
- **Risk Analytics**: CAGR, Sharpe Ratio, Volatility, Max Drawdown, Alpha, Beta
- **Performance Reports**: JSON, TXT, PDF, and interactive HTML formats
- **Streamlit Dashboard** for live exploration
- **26 years of data** (2000–2026) from Yahoo Finance

## Quick Start

```bash
pip install -r requirements.txt
python main.py          # Download data
python run_backtest.py  # Run backtests
streamlit run dashboard/app.py  # Launch dashboard
```

## Results

Open `reports/combined_report.html` for the full interactive report with charts, tables, conclusions, and recommendations.

## Screenshots

![Benchmark & Stock Comparison](Screenshots/Screenshot%202026-05-22%20at%201.03.15%E2%80%AFPM.png)
![Backtest Results Table](Screenshots/Screenshot%202026-05-22%20at%201.10.32%E2%80%AFPM.png)
![Strategy Comparison](Screenshots/Screenshot%202026-05-22%20at%201.10.37%E2%80%AFPM.png)
![Performance Charts](Screenshots/Screenshot%202026-05-22%20at%201.10.41%E2%80%AFPM.png)
![Equity Curves](Screenshots/Screenshot%202026-05-22%20at%201.10.45%E2%80%AFPM.png)
![Risk Analysis](Screenshots/Screenshot%202026-05-22%20at%201.10.48%E2%80%AFPM.png)
![Conclusions](Screenshots/Screenshot%202026-05-22%20at%201.10.52%E2%80%AFPM.png)
![Recommendations](Screenshots/Screenshot%202026-05-22%20at%201.10.56%E2%80%AFPM.png)
![Detailed Stock View](Screenshots/Screenshot%202026-05-22%20at%201.11.00%E2%80%AFPM.png)
![Dashboard Preview](Screenshots/Screenshot%202026-05-22%20at%201.11.07%E2%80%AFPM.png)

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

pandas, numpy, yfinance, backtesting, plotly, streamlit, scipy, statsmodels, quantstats, vectorbt, fpdf2
