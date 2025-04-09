import os
from sqlalchemy import create_engine
import yfinance as yf
import urllib.parse
from dotenv import load_dotenv  # Import the load_dotenv function

# Load environment variables from the .env file
load_dotenv()


# Define the stock data fetching function
def fetch_stock_data(ticker, start, end):
    """
    Fetch stock data using Yahoo Finance.
    :param ticker: Stock ticker symbol (e.g., "AAPL").
    :param start: Start date for data (e.g., "2023-01-01").
    :param end: End date for data (e.g., "2025-04-08").
    :return: Pandas DataFrame with the stock data.
    """
    stock_data = yf.download(ticker, start=start, end=end, auto_adjust=True)

    # Reset the index to add the 'Date' as a column
    stock_data.reset_index(inplace=True)  # This will move the 'Date' from index to a column

    return stock_data


# Database connection function
def save_to_postgres(df, ticker):
    """
    Save the stock data to PostgreSQL database.
    :param df: Pandas DataFrame containing the stock data.
    :param ticker: The name of the table in the database.
    """
    # Load database credentials from environment variables
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # URL-encode the password to handle special characters like "@"
    encoded_password = urllib.parse.quote(DB_PASSWORD)

    DATABASE_URL = f"postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create a connection engine
    engine = create_engine(DATABASE_URL)

    # Save DataFrame to PostgreSQL
    df.to_sql(ticker, con=engine, if_exists='replace', index=False)


# Main function to fetch data and save to PostgreSQL
if __name__ == "__main__":
    # Example: Fetch Apple stock data from Jan 1, 2023 to today
    df = fetch_stock_data("AAPL", start="2023-01-01", end="2025-04-08")

    # Save the data to PostgreSQL
    save_to_postgres(df, "aapl_stock_data")

    print("Stock data has been successfully saved to PostgreSQL.")
