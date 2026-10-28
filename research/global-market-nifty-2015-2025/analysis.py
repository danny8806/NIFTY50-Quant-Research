#!/usr/bin/env python3
"""Reproduce cross-market / NIFTY daily-return study (2015–2025).

All outcomes are historical associations. Same-day Asian closes are EX-POST.
Usage: pip install -r requirements.txt && python analysis.py
"""
from __future__ import annotations

import argparse
import io
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

START, END = "2015-01-01", "2025-12-31"
BASE = "https://raw.githubusercontent.com/Hareeshkesavan/Stock-Market-Dataset/main/"
FILES = {
    "nifty": "Nifty 50 Historical Data.csv",
    "sp": "S&P 500 Historical Data.csv",
    "nikkei": "Nikkei 225 Historical Data.csv",
    "hang_seng": "Hang Seng Historical Data.csv",
    "shanghai": "Shanghai Composite Historical Data.csv",
    "ftse": "FTSE 100 Historical Data.csv",
    "brent": "Brent Oil Futures Historical Data.csv",
    "vix": "CBOE Volatility Index Historical Data.csv",
}
LABELS = {"sp": "S&P 500 (previous US close)",
          "nikkei": "Nikkei 225 (same-day close, ex-post)",
          "hang_seng": "Hang Seng (same-day close, ex-post)",
          "shanghai": "Shanghai Composite (same-day close, ex-post)",
          "ftse": "FTSE 100 (previous UK close)",
          "brent": "Brent (previous close)",
          "vix": "US VIX (previous close)"}


def read_market(key: str, offline_dir: Path | None = None) -> pd.DataFrame:
    filename = FILES[key]
    if offline_dir:
        content = (offline_dir / filename).read_bytes()
    else:
        req = Request(BASE + quote(filename),
                      headers={"User-Agent": "GlobalNiftyResearch/1.0"})
        with urlopen(req, timeout=45) as response:
            content = response.read()
    df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig", dtype=str)
    if not {"Date", "Price", "Open", "High", "Low"}.issubset(df.columns):
        raise ValueError(f"Missing OHLC fields in {filename}")
    df["date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="raise")
    for name, col in [("close", "Price"), ("open", "Open"),
                      ("high", "High"), ("low", "Low")]:
        df[name] = pd.to_numeric(df[col].str.replace(",", "", regex=False),
                                 errors="raise")
    if df.date.duplicated().any():
        raise ValueError(f"Duplicate dates in {filename}")
    if (df[["close", "open", "high", "low"]] <= 0).any().any():
        raise ValueError(f"Nonpositive OHLC in {filename}")
    if (df.high < df.low).any():
        raise ValueError(f"Invalid high/low in {filename}")
    df = df.sort_values("date").reset_index(drop=True)
    df["return_pct"] = df.close.pct_change() * 100
    return df[df.date.between(START, END)].copy()


def align(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    n = raw["nifty"].copy()
    # Retain exceptional Indian weekend sessions when computing prior close.
    n["previous_close"] = n.close.shift(1)
    n["nifty_pct"] = 100 * (n.close / n.previous_close - 1)
    n["gap_pct"] = 100 * (n.open / n.previous_close - 1)
    n["intraday_pct"] = 100 * (n.close / n.open - 1)
    n = n[(n.date.dt.weekday < 5) & n.previous_close.notna()]
    combined = n[["date", "nifty_pct", "gap_pct", "intraday_pct"]].copy()
    for key, data in raw.items():
        if key == "nifty":
            continue
        data = data.loc[data.date.dt.weekday < 5].copy()
        if key in {"nikkei", "hang_seng", "shanghai"}:
            # Asian same-day close is unavailable BEFORE the NIFTY opening.
            paired = data[["date", "return_pct"]].rename(
                columns={"return_pct": key})
            combined = combined.merge(paired, how="left", on="date",
                                      validate="one_to_one")
        else:
            # Previous COMPLETE foreign session is available before 09:15 IST.
            other = data[["date", "return_pct"]].rename(
                columns={"date": f"{key}_date", "return_pct": key})
            combined = pd.merge_asof(combined.sort_values("date"),
                                     other.sort_values(f"{key}_date"),
                                     left_on="date", right_on=f"{key}_date",
                                     allow_exact_matches=False,
                                     direction="backward")
            valid = combined[f"{key}_date"].notna()
            assert (combined.loc[valid, f"{key}_date"] <
                    combined.loc[valid, "date"]).all(), "Future leakage"
    return combined


def correlations(aligned: pd.DataFrame) -> pd.DataFrame:
    out = []
    for key, label in LABELS.items():
        x = aligned[[key, "nifty_pct", "gap_pct", "intraday_pct"]].dropna()
        out.append({
            "market": key, "label": label, "count": len(x),
            "full_day_corr": x[key].corr(x.nifty_pct),
            "gap_corr": x[key].corr(x.gap_pct),
            "intraday_corr": x[key].corr(x.intraday_pct),
            "same_sign_pct": 100 * ((x[key] * x.nifty_pct) > 0).mean(),
        })
    return pd.DataFrame(out)


def conditional(a: pd.DataFrame) -> pd.DataFrame:
    x = a.dropna(subset=["sp"])
    out = []
    groups = [("S&P >= +1%", x.sp >= 1), ("S&P <= -1%", x.sp <= -1),
              ("S&P > 0%", x.sp > 0), ("S&P < 0%", x.sp < 0),
              ("All paired days", pd.Series(True, index=x.index))]
    for label, mask in groups:
        z = x.loc[mask]
        out.append({
            "condition": label, "count": len(z),
            "gap_up_pct": 100 * (z.gap_pct > 0).mean(),
            "close_up_pct": 100 * (z.nifty_pct > 0).mean(),
            "intraday_up_pct": 100 * (z.intraday_pct > 0).mean(),
            "mean_gap_pct": z.gap_pct.mean(),
            "mean_full_day_pct": z.nifty_pct.mean(),
            "mean_intraday_pct": z.intraday_pct.mean(),
        })
    return pd.DataFrame(out)


def periods(a: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for label, data in [
        ("2015-2019", a[a.date < "2020-01-01"]),
        ("2020", a[a.date.between("2020-01-01", "2020-12-31")]),
        ("2021-2025", a[a.date >= "2021-01-01"]),
    ]:
        t = conditional(data).head(2).copy()
        t.insert(0, "period", label)
        frames.append(t)
    return pd.concat(frames, ignore_index=True)


def plot_results(c: pd.DataFrame, s: pd.DataFrame, p: pd.DataFrame,
                 folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    focus = c.set_index("market").loc[["sp", "nikkei", "hang_seng",
                                       "shanghai", "ftse"]]
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=180)
    y = np.arange(len(focus))
    for offset, key, label in [(-.24, "gap_corr", "Opening gap"),
                               (0, "full_day_corr", "Full day"),
                               (.24, "intraday_corr", "Intraday")]:
        ax.barh(y + offset, focus[key], height=.23, label=label)
    ax.set_yticks(y, ["S&P 500", "Nikkei", "Hang Seng", "Shanghai", "FTSE 100"])
    ax.invert_yaxis()
    ax.axvline(0, color="black", linewidth=.7)
    ax.set_xlim(-.14, .65)
    ax.set_title("Global correlations with NIFTY returns | 2015-2025")
    ax.set_xlabel("Pearson correlation")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=.15)
    fig.tight_layout()
    fig.savefig(folder / "correlations.png")
    fig.savefig(folder / "correlations.svg")
    plt.close(fig)

    focus = s.head(2)
    up_gap = focus.gap_up_pct.to_numpy()
    up_close = focus.close_up_pct.to_numpy()
    values_gap = [up_gap[0], 100 - up_gap[1]]
    values_close = [up_close[0], 100 - up_close[1]]
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=180)
    y = np.arange(2)
    ax.barh(y - .19, values_gap, .36, label="Opening follows US sign")
    ax.barh(y + .19, values_close, .36, label="Closing follows US sign")
    for j in range(2):
        ax.text(values_gap[j] + 1, y[j] - .19, f"{values_gap[j]:.1f}%", va="center")
        ax.text(values_close[j] + 1, y[j] + .19, f"{values_close[j]:.1f}%", va="center")
    ax.set_yticks(y, [f"US >=+1% (n={focus.iloc[0]['count']})",
                      f"US <=-1% (n={focus.iloc[1]['count']})"])
    ax.invert_yaxis()
    ax.set_xlim(0, 105)
    ax.set_xlabel("Same-direction frequency (%)")
    ax.set_title("US +/-1%: NIFTY opening vs closing | 2015-2025")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=.15)
    fig.tight_layout()
    fig.savefig(folder / "us_thresholds.png")
    fig.savefig(folder / "us_thresholds.svg")
    plt.close(fig)

    focus = p[p.period != "2020"]
    fig, axs = plt.subplots(1, 2, figsize=(11, 5), sharey=True, dpi=180)
    for axis, condition in zip(axs, ["S&P >= +1%", "S&P <= -1%"]):
        z = focus[focus.condition == condition]
        vals = z.gap_up_pct.to_numpy()
        if "<=" in condition:
            vals = 100 - vals
        axis.bar(z.period, vals)
        for i, val in enumerate(vals):
            axis.text(i, val + 1, f"{val:.1f}%", ha="center")
        axis.set_ylim(0, 105)
        axis.set_title(condition)
        axis.grid(axis="y", alpha=.15)
    axs[0].set_ylabel("Gap follows US direction (%)")
    fig.suptitle("Subperiod stability: previous S&P vs NIFTY opening")
    fig.tight_layout()
    fig.savefig(folder / "period_stability.png")
    fig.savefig(folder / "period_stability.svg")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=None,
                        help="Folder containing exact eight source filenames")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).parent / "output")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw = {name: read_market(name, args.input_dir) for name in FILES}
    a = align(raw)
    c, s, p = correlations(a), conditional(a), periods(a)
    for name, frame in [("aligned_daily_returns", a), ("correlations", c),
                        ("conditional_us", s), ("period_stability", p)]:
        frame.to_csv(args.output_dir / f"{name}.csv", index=False)
    plot_results(c, s, p, args.output_dir / "plots")
    print("Ordinary NIFTY weekday sessions:", len(a))
    print(c.round(3).to_string(index=False))
    print(s.round(3).to_string(index=False))
    print("Saved:", args.output_dir)


if __name__ == "__main__":
    main()
