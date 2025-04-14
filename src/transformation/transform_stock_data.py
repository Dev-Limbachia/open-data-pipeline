import pandas as pd
from src.utils.database_connection import get_db_engine

engine = get_db_engine()


def transform_group(df):
    """
    Perform transformation for a single ticker's data.
    """
    # Sort by date (important for rolling calculations)
    df = df.sort_values(by='date')

    # Calculate daily return (%)
    df['daily_return'] = ((df['close'] - df['open']) / df['open']) * 100

    # Calculate volatility: (high - low)/open * 100
    df['volatility'] = ((df['high'] - df['low']) / df['open']) * 100

    # Price difference: close - open
    df['price_diff'] = df['close'] - df['open']

    # Gain day indicator: 1 if close > open, else 0
    df['is_gain_day'] = (df['close'] > df['open']).astype(int)

    # Calculate 7-day moving average of close price
    df['7d_ma'] = df['close'].rolling(window=7, min_periods=1).mean()

    # Calculate 30-day moving average of close price
    df['30d_ma'] = df['close'].rolling(window=30, min_periods=1).mean()

    return df


def transform_stock_data():
    # Step 1: Read raw data from the unified table "stock_prices"
    df = pd.read_sql("SELECT * FROM stock_prices", con=engine)
    if df.empty:
        print("No data found in the raw stock_prices table.")
        return

    # Step 2: Ensure that the 'date' column is of datetime type
    df['date'] = pd.to_datetime(df['date'])

    # (Optional) Print some basic info for debugging
    print("Raw data sample:")
    print(df.head())

    # Step 3: Group the data by ticker and apply the transformation function
    transformed = df.groupby('ticker').apply(transform_group).reset_index(drop=True)

    # (Optional) Print a sample of transformed data for verification
    print("Transformed data sample:")
    print(transformed.head())

    # Step 4: Write the transformed data to a new table
    transformed.to_sql("stock_prices_transformed", con=engine, if_exists='replace', index=False)
    print("✅ Transformed data saved successfully to table: stock_prices_transformed")


if __name__ == "__main__":
    transform_stock_data()
