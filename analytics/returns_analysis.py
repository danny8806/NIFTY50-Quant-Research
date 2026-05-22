
import numpy as np

def daily_returns(df):
    return df['Close'].pct_change()

def log_returns(df):
    return np.log(df['Close'] / df['Close'].shift(1))

def cagr(df):
    total_return = df['Close'].iloc[-1] / df['Close'].iloc[0]
    years = len(df) / 252
    return (total_return ** (1 / years)) - 1
