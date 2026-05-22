
from config.settings import STOCKS, BENCHMARK, START_DATE, END_DATE
from utils.data_loader import download_stock_data, save_data
import os

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/benchmark", exist_ok=True)

for stock in STOCKS:
    print(f"Downloading {stock}")

    df = download_stock_data(
        stock,
        START_DATE,
        END_DATE
    )

    save_data(df, f"data/raw/{stock}.csv")

benchmark = download_stock_data(
    BENCHMARK,
    START_DATE,
    END_DATE
)

save_data(
    benchmark,
    "data/benchmark/nifty50.csv"
)

print("All data downloaded successfully")
