# LinkedIn post and charts — draft, NOT published

Attach the research plots (preferably PNG exported from analysis.py) in this order:
1. plots/us_thresholds.svg (opening vs closing signal effect)
2. plots/correlation_overview.svg (correlations)
3. plots/period_stability.svg (historical subperiod stability)

Proposed post:

Can global stock markets predict NIFTY — or do they mostly explain India's opening gap?

I analyzed 11 years (2015–2025) of daily market observations comparing NIFTY 50 with previous-session S&P 500 returns.

Here is what stood out:

• Following a previous S&P 500 gain of at least 1%, NIFTY opened higher in **91.2%** of 362 matched sessions — but closed higher in only **67.4%**.

• After a previous S&P 500 drop of at least 1%, NIFTY opened lower in **74.6%** of 295 matched sessions.

• Prior US returns correlated **+0.479** with NIFTY's opening gap, but only **-0.030** with the subsequent NIFTY intraday return.

Interpretation: overseas risk sentiment has a clear historical relationship with the Indian OPEN, not necessarily an after-open trading edge.

A necessary caveat: these are retrospective descriptive associations — not live prediction accuracy or backtested profit. NIFTY opened higher on roughly 68% of the sample sessions even without filtering on the US market. Same-day final Asian closes are also NOT available at 9:15 IST, so they cannot be used in a leak-free pre-open model.

Full reproducible Python code, source notes, charts and limitations:
https://github.com/danny8806/NIFTY50-Quant-Research/tree/main/research/global-market-nifty-2015-2025

Next test: 09:00 IST live Asian quotes + GIFT Nifty + oil + USD/INR + India VIX, evaluated chronologically and with executable fills.

#NIFTY50 #QuantResearch #IndianStockMarket #DataScience #Python #FinancialMarkets

---

Publishing requires your connected LinkedIn/social publishing account and review of final visual assets.
