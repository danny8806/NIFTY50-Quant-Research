
import yfinance as yf
import pandas as pd

def download_stock_data(symbol, start, end):
    df = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True
    )
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.dropna(inplace=True)
    return df

def save_data(df, path):
    df.to_csv(path)

def load_data(path):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.dropna(inplace=True)
    return df
