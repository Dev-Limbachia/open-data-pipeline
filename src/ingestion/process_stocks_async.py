import asyncio
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from fetch_stock_data import fetch_stock_data
from save_to_postgres import save_to_postgres


def process_stock_row(row):
    ticker, start, end = row['ticker'], row['start_date'], row['end_date']
    print(f"Fetching data for {ticker}...")
    df = fetch_stock_data(ticker, start, end)
    if not df.empty:
        save_to_postgres(df, ticker)
        print(f"✅ {ticker} saved successfully.")
    else:
        print(f"❌ No data found for {ticker}.")


async def main():
    df_tickers = pd.read_csv("tickers.csv")

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [
            loop.run_in_executor(executor, process_stock_row, row)
            for _, row in df_tickers.iterrows()
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
