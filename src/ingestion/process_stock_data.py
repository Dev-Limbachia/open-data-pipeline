import pandas as pd
from fetch_stock_data import fetch_stock_data
from save_to_postgres import save_to_postgres


def process_stock_row(row):
    ticker, start, end = row['ticker'], row['start_date'], row['end_date']
    print(f"Fetching data for {ticker}...")
    df = fetch_stock_data(ticker, start, end)
    if not df.empty:
        save_to_postgres(df, "stock_prices")
        print(f"✅ {ticker} saved successfully.")
    else:
        print(f"❌ No data found for {ticker}.")


def main():
    df_tickers = pd.read_csv("tickers.csv")

    for _, row in df_tickers.iterrows():
        # Create a true copy of the row to avoid shared references
        row = row.copy()

        ticker = row['ticker']
        start = row['start_date']
        end = row['end_date']

        print(f"Fetching data for {ticker}...")
        df = fetch_stock_data(ticker, start, end)

        if not df.empty:
            # Reset index to make 'Date' a column
            df.reset_index(inplace=True)

            # Flatten MultiIndex columns, if present
            df.columns = ['_'.join(col).lower().strip() if isinstance(col, tuple) else col.lower().strip() for col in
                          df.columns]

            # Rename columns if necessary
            rename_map = {}
            for col in df.columns:
                if 'open' in col: rename_map[col] = 'open'
                if 'high' in col: rename_map[col] = 'high'
                if 'low' in col: rename_map[col] = 'low'
                if 'close' in col: rename_map[col] = 'close'
                if 'volume' in col: rename_map[col] = 'volume'
                if 'date' in col: rename_map[col] = 'date'

            df.rename(columns=rename_map, inplace=True)

            # Add ticker and reorder columns
            df['ticker'] = ticker.upper()
            df = df[['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']]
            df.dropna(subset=["open", "close"], inplace=True)

            # ✅ Save raw CSV as before
            df.to_csv(f"data/{ticker.lower()}_raw.csv", index=False)

            # ✅ Save to Postgres
            save_to_postgres(df, table_name="stock_prices")

            print(f"✅ {ticker} saved successfully.")
        else:
            print(f"❌ No data found for {ticker}.")


if __name__ == "__main__":
    main()
