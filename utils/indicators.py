
import pandas as pd
import numpy as np

def ema(series, period):
    s = pd.Series(series)
    return s.ewm(span=period, adjust=False).mean().values

def sma(series, period):
    s = pd.Series(series)
    return s.rolling(period).mean().values

def rsi(series, period=14):
    s = pd.Series(series)
    delta = s.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return (100 - (100 / (1 + rs))).values
