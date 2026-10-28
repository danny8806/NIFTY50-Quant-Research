# Detailed findings (frozen 2015–2025 historical snapshot)

## 1. Global US vs NIFTY opening

For **2,713** ordinary NIFTY weekdays paired with the previous completed S&P 500 session:
- Correlation of S&P prior daily returns with next NIFTY opening gap: **+0.479**.
- Correlation with full-day NIFTY close-to-close return: **+0.268**.
- Correlation with NIFTY open-to-close return: **-0.030**.

Interpretation: shared global risk sentiment tends to be reflected in the Indian opening; prior US daily returns show little linear relationship with subsequent NIFTY intraday return.

## 2. Large previous US moves

| Prior S&P move | Sample | Next NIFTY gap-up | Next NIFTY close-up | Average NIFTY gap |
|---|---:|---:|---:|---:|
| >= +1% | 362 | 91.2% | 67.4% | +0.524% |
| <= -1% | 295 | 25.4% | 33.2% | -0.503% |

Thus a prior S&P <=-1% coincided with NIFTY gap-DOWN **74.6%** of the time, and close-DOWN **66.8%** of the time.

**Compare against the unconditional baseline:** ordinary NIFTY matched sessions opened higher **68.0%** and closed higher **53.8%** of the time. These percentages do not represent realizable trade returns or validated prediction accuracy.

After prior S&P >=+1%, average *open-to-close* NIFTY return was about **-0.102%**: the relationship mostly appears before the regular-session trade entry would execute.

## 3. Subperiods

| Prior US signal and outcome | 2015–2019 | 2021–2025 |
|---|---:|---:|
| S&P >=+1%, NIFTY gap-up | 93.5%, n=123 | 90.9%, n=176 |
| S&P <=-1%, NIFTY gap-down | 71.3%, n=101 | 78.4%, n=153 |

Descriptive robustness across time, not a separate out-of-sample test.

## 4. Same-day Asian market correlation: ex-post ONLY

| Asian index | Sample | NIFTY gap correlation | NIFTY full-day correlation |
|---|---:|---:|---:|
| Nikkei 225 | 2,538 | +0.469 | +0.358 |
| Hang Seng | 2,585 | +0.441 | +0.402 |
| Shanghai Composite | 2,540 | +0.267 | +0.214 |

**Look-ahead danger:** The Asian numbers use *that same day's final closing return*, which was not known when India opened. These statistics do NOT establish premarket predictive value.

## 5. Prioritized next tests

- Does US movement improve NIFTY intraday prediction after conditioning on **GIFT Nifty** and observed opening gap?
- Is there a difference between positive and negative global-news deviations after controlling for oil and domestic results?
- Does the relationship change when US VIX rises more than 10%, on major Fed/RBI dates, or when Indian institutional flows oppose the US direction?
- Which feature combinations remain stable using *timestamp-accurate* 09:00 IST snapshots, chronologically separated tests and execution-feasible fills?

Reproduce via analysis.py and verify against official source histories before production use. NOT investment advice.
