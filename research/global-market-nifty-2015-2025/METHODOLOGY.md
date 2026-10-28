# Methodology, data provenance and look-ahead controls

## Source

Public third-party GitHub mirror: https://github.com/Hareeshkesavan/Stock-Market-Dataset

Daily OHLC files used:
1. Nifty 50 Historical Data.csv
2. S&P 500 Historical Data.csv
3. Nikkei 225 Historical Data.csv
4. Hang Seng Historical Data.csv
5. Shanghai Composite Historical Data.csv
6. FTSE 100 Historical Data.csv
7. Brent Oil Futures Historical Data.csv
8. CBOE Volatility Index Historical Data.csv

Data were inspected in October 2026. All study observations are restricted to 2015-01-01 through 2025-12-31. The public historical mirror is not an official exchange feed and its values can be revised. Raw source files are downloaded by the analysis script instead of committed here.

**Spot cross-check:** Among 1,214 NIFTY closing levels overlapping between this source and https://github.com/VatsalSin/Stock-Market-Indices-Dataset during 2015–2019, 1,213 matched within 0.02 index points; one differed by 0.45 index points (2018-11-07). This is a limited check, not comprehensive exchange-grade validation.

## Return definitions

- Full-day NIFTY return (%) = 100 * (Close(today) / Close(previous NIFTY session) - 1).
- NIFTY opening gap (%) = 100 * (Open(today) / Close(previous NIFTY session) - 1).
- NIFTY intraday (%) = 100 * (Close(today) / Open(today) - 1).
- Pearson correlation = correlation of paired observed daily percent returns, not index levels.
- Same-direction frequency = count(matching sign) / count(paired observations).
- Conditional probabilities = observations meeting outcome / observations meeting the global-market condition.

NIFTY **weekend special sessions** (e.g. Budget or Muhurat) must be included when calculating the preceding NIFTY close. Only after that step are results restricted to ordinary Monday–Friday Indian sessions. Do not forward-fill missing foreign daily RETURNS over holidays. Match the prior *actually completed* foreign trading session, not always calendar day minus one.

## Timing audit

| Variable | Alignment | Available at India's 09:15 opening? |
|---|---|---|
| Prior US S&P 500 closing return | Latest US session with date STRICTLY BEFORE NIFTY session | Yes |
| Prior FTSE closing return | Latest UK session strictly before NIFTY session | Yes |
| Prior completed US VIX and Brent closing return | Last foreign session strictly before NIFTY date | Usually, subject to venue time checks |
| Nikkei/Hang Seng/Shanghai same-calendar-date **final** return | Same date completed close | **No: descriptive / ex-post ONLY** |
| NIFTY opening gap | Current Indian open vs previous Indian close | Becomes known only at opening |
| NIFTY close / open-to-close return | Current Indian close | **No** |

No future foreign close from the same date is used in pre-open-aligned US features. The script uses backward-asof joins with allow_exact_matches=False for previous foreign sessions.

**Do NOT use the Asian same-day *closing* correlations as predictive evidence for 09:15 trading.** For a valid model use live quoted values as of 09:00 IST or the last *fully completed* session.

## Baselines and limitations

- Sample: 2,713 ordinary NIFTY weekdays with a paired previous completed S&P 500 return.
- Baseline: approximately 68% of these sessions have a positive NIFTY opening gap regardless of US movement.
- All reported percentages are IN-SAMPLE and observational. No transaction-cost or fill model, significance test, predictive holdout, bootstrap confidence interval, causal inference or controlled experiment was performed.
- No inference is made that the opening return can be captured with an order sent after the opening.
- Daily OHLC sources can contain discrepancies, exchange closures, stale/corrected prices and index-adjustment differences.
- Compare subperiods but do not treat those retrospectively chosen subperiods as an unseen test set.

## Research extension protocol

1. Archive timestamped data for last completed US session, 09:00 IST GIFT Nifty/Asian quotes, crude, USD/INR, published investor flows and India VIX.
2. Construct three distinct targets: pre-open gap direction, NIFTY open-to-10:00 and NIFTY open-to-15:30.
3. Use expanding walk-forward splits, purging where targets overlap, and final untouched holdouts.
4. Compare majority-class baseline, volatility-only, GIFT Nifty and simple linear models before complex ML.
5. Evaluate calibrated probabilities, precision, base rates, rolling stability, slippage, costs, drawdowns and missing data.
6. Publish null results and confidence intervals; avoid cherry-picked thresholds or trade simulations that use future values.

Source use/licensing and trading data redistribution rights should be checked independently before commercial reuse.
