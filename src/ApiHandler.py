
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf


def interval_request (ticker: str, start: str, end : str, interval_size):
    try:
        data = yf.download(ticker, start=start, end=end, interval=interval_size)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


def data_request (ticker: str, years: int, interval_size: str):
    current_date = dt.datetime.now().date()
    start_date = current_date - dt.timedelta(days=years * 365) # this day n years ago
    return interval_request(ticker, start_date, current_date, interval_size)


"""
data = data_request("SPY", 20, "1wk")
data['Close'].plot()
plt.title("Apple Stock Prices")
plt.show()
"""

        



