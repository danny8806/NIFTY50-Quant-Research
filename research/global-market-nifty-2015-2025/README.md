# Global markets vs NIFTY 50 | Historical evidence (2015–2025)

![Global correlation chart](plots/correlation_overview.svg)

**Research objective:** quantify when NIFTY follows the previous completed US session and when global sentiment is reflected primarily in India's *opening gap*, rather than its *intraday price change*.

**Scope:** 1 January 2015 to 31 December 2025. This is a retrospective descriptive study, NOT live trading-model accuracy, a causal analysis, or a profit backtest. The source is a public third-party daily OHLC dataset, not official exchange data.

## Headline findings

| Previous S&P 500 close-to-close move | NIFTY opened in same direction | NIFTY closed in same direction | Observations |
|---|---:|---:|---:|
| +1% or more | **91.2%** (gap-up) | **67.4%** (close-up) | 362 |
| -1% or less | **74.6%** (gap-down) | **66.8%** (close-down) | 295 |

![Large US moves and Indian outcomes](plots/us_thresholds.svg)

**Baseline matters:** NIFTY opened above the previous close on roughly **68.0%** of the matched ordinary weekday sessions *regardless* of the US signal. High gap-up frequency is not proof of an exploitable strategy: a trader cannot necessarily fill at the previous Indian close after seeing the US session.

## Where the statistical relationship appears

| Global index | Matched sessions | NIFTY gap correlation | NIFTY full-day correlation | NIFTY intraday correlation |
|---|---:|---:|---:|---:|
| S&P 500, **previous** completed US session | 2,713 | **+0.479** | +0.268 | **-0.030** |
| Nikkei 225, **same-day closing** return | 2,538 | +0.469 | +0.358 | +0.084 |
| Hang Seng, **same-day closing** return | 2,585 | +0.441 | +0.402 | +0.161 |
| Shanghai Composite, **same-day closing** return | 2,540 | +0.267 | +0.214 | +0.062 |

**Critical timestamp rule:** The Asian indices' *same-day final closing values* are not available before India's 09:15 AM open. Those three comparisons are ex-post descriptions ONLY. They cannot be used as predictive features for NIFTY's opening without look-ahead bias.

![Historical comparison across subperiods](plots/period_stability.svg)

## Period stability

| Previous US signal | 2015–2019 | 2021–2025 |
|---|---:|---:|
| S&P +1% or more, NIFTY opens higher | 93.5% (n=123) | 90.9% (n=176) |
| S&P -1% or less, NIFTY opens lower | 71.3% (n=101) | 78.4% (n=153) |

The 2020 market-shock period is not folded into either comparison; the analysis script exports it separately. These subperiods were assessed retrospectively, not as untouched independent model tests.

## Reproduce the results

From this research directory, run:

    python -m pip install -r requirements.txt
    python analysis.py

The script downloads eight source CSV files, validates columns, aligns market sessions correctly and writes the following to an uncommitted output directory:

    output/aligned_daily_returns.csv
    output/correlations.csv
    output/conditional_us.csv
    output/period_stability.csv
    output/plots/correlations.png (+ .svg)
    output/plots/us_thresholds.png (+ .svg)
    output/plots/period_stability.png (+ .svg)

For reproducibility without network access, download the eight source CSV files listed in METHODOLOGY.md into one directory, then run:

    python analysis.py --input-dir /path/to/csv-folder

The source owner may revise their files. The checked-in SVG graphs are *frozen illustration snapshots* of the calculations described here. Rerun the script for auditable calculations and generated PNG/SVG charts.

## Project files

- **analysis.py** — end-to-end Python data ingestion, return alignment, analytics, charts.
- **METHODOLOGY.md** — sources, date alignment, special-session handling, validity limits.
- **RESULTS.md** — descriptive findings and hypotheses for future testing.
- **data/snapshot_metrics.csv** — independently documented frozen summary statistics.
- **plots/** — GitHub-embeddable SVG snapshots.

## Main conclusion

The previous S&P 500 session is correlated with NIFTY's *opening gap* considerably more than with NIFTY's *after-open intraday return*. The headline 91.2% conditional opening frequency does **not** imply one could earn that return by placing an order at 09:15.

An appropriate next research step is a point-in-time dataset: 09:00 IST GIFT Nifty and Asian quotes, US close, crude, USD/INR, India VIX and prior-published FII/DII. Then test NIFTY intraday outcomes using chronological walk-forward experiments, execution costs and robust baselines.

**Research/education only. Not investment advice.**
