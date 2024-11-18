import pandas as pd
import yfinance as yf
from utils import get_previous_date, get_next_date, get_date_time_object_from_string

def get_stock_price_data(ticker, date):
    # Give date in the form of YYYY-MM-DD
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=date, end=get_next_date(date))
    if historical_data.empty:
        return None
    return float(historical_data.iloc[0]['Close'])

def get_company_financials(ticker, date):
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=date, end=get_next_date(date))
    if historical_data.empty:
        return None
    return historical_data

def get_stock_price_data_range(ticker, date, interval=10):
    # Give date in the form of YYYY-MM-DD
    results = pd.DataFrame()
    while len(results) < interval:
        date = get_previous_date(date)
        data = get_company_financials(ticker, date)
        if data is not None:
            results = pd.concat([results, data], ignore_index=True)
    return results