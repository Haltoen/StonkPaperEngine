
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
from pytz import timezone

def is_market_open(ticker):
    try: # test connection
        ticker_data = yf.Ticker(ticker).info # retrive ticker data
    except Exception as e:
        print(f"An error occurred: {e}") 
        return False

    if ticker_data["quoteType"] == "CRYPTOCURRENCY": return True # Crypto allways open
    else:
        exchange_timezone = ticker_data["timeZoneShortName"] # get stock timeZone
        tz = timezone(exchange_timezone)
        
        # Assuming NYSE trading hours are from 9:30 AM to 4:00 PM
        current_time = dt.datetime.now(tz).time()
        market_open_time = dt.time(9, 30)
        market_close_time = dt.time(16, 0)

        return market_open_time <= current_time <= market_close_time


def interval_request (ticker: str, start: str, interval_size):
    try: # test connection
        data = yf.download(ticker, start=start, interval=interval_size)
        return data
    except Exception as e:
        print(f"An error occurred: {e}") 
        return False


def data_request (ticker: str, days: int, interval_size: str):

    current_date = dt.datetime.now(tz=timezone("UTC")).date()
    start_date = dt.datetime.combine(current_date - dt.timedelta(days=days-1), dt.time())
    print(current_date)
    print(start_date)
    # request intercval data
    data = interval_request(ticker, start_date, interval_size)
    
    return data



"""
print(yf.Ticker("btc-usd").info["timeZoneShortName"])
print(yf.Ticker("btc-usd").info["priceHint"])
print(yf.Ticker("eth-btc").info["quoteType"])
"""