import os
import urllib

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# DB Credentials
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def transform_stock_data(ticker: str):
    # Read raw data from DB
    raw_table = ticker.lower()
    df = pd.read_sql(f"SELECT * FROM {raw_table}", con=engine)

    # Debugging step: Print the column names to check if 'Close' exists
    print(f"Columns in the {raw_table} table:", df.columns)

    # Optionally: Print the first few rows to verify the data
    print(df.head())

    # === Begin Transformations ===
    try:
        # Debugging step: Ensure the column names are clean and stripped of spaces
        df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
        print(f"Cleaned columns: {df.columns}")

        # Check if 'Close' column exists
        if 'Close' not in df.columns:
            raise KeyError("'Close' column not found in the DataFrame!")

        # Perform the transformations
        df['daily_return'] = ((df['Close'] - df['Open']) / df['Open']) * 100
        df['volatility'] = ((df['High'] - df['Low']) / df['Open']) * 100
        df['price_diff'] = df['Close'] - df['Open']
        df['is_gain_day'] = (df['Close'] > df['Open']).astype(int)

        # Moving averages
        df['7d_ma'] = df['Close'].rolling(window=7).mean()
        df['30d_ma'] = df['Close'].rolling(window=30).mean()

    except KeyError as e:
        print(f"Error: {e}")
        return  # Skip this ticker if column is missing

    # Save to new table
    transformed_table = f"{ticker.lower()}_stock_transformed"
    df.to_sql(transformed_table, con=engine, if_exists='replace', index=False)
    print(f"✅ Transformed data saved to table: {transformed_table}")


if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'TSLA']  # Update as needed
    for ticker in tickers:
        transform_stock_data(ticker)