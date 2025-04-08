import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

def save_to_csv(df: pd.DataFrame, ticker: str):
    date_str = datetime.today().strftime('%Y-%m-%d')
    filename = f"data/{ticker}_{date_str}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    # Example: Apple stock from Jan 1, 2023 to today
    df = fetch_stock_data("AAPL", start="2023-01-01", end=datetime.today().strftime('%Y-%m-%d'))
    save_to_csv(df, "AAPL")
