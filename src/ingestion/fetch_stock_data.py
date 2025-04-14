import yfinance as yf


def fetch_stock_data(ticker, start, end):
    """
    Fetch stock data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    data.reset_index(inplace=True)  # 'Date' as a column
    return data
