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

def get_company_stock_history(ticker, date):
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=date, end=get_next_date(date))
    if historical_data.empty:
        return None
    historical_data['Date'] = historical_data.index
    historical_data['Date'] = historical_data['Date'].dt.date
    return historical_data

def get_stock_price_data_range(ticker, date, interval=10):
    # Give date in the form of YYYY-MM-DD
    results = pd.DataFrame()
    while len(results) < interval:
        date = get_previous_date(date)
        data = get_company_stock_history(ticker, date)
        if data is not None:
            results = pd.concat([results, data], ignore_index=True)
    results = results.iloc[::-1].reset_index(drop=True)
    return results

def get_company_financials(df):
    df_features = pd.DataFrame()
    df_features['Date'] = df['Date']
    df_features['Daily Pct Change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df_features['Volume Trend (5-Day MA)'] = df['Volume'].rolling(window=5).mean()
    df_features['5-Day Moving Avg'] = df['Close'].rolling(window=5).mean()
    df_features['Daily Volatility'] = ((df['High'] - df['Low']) / df['Open']) * 100
    df_features['Prev Day Close'] = df['Close'].shift(1)
    return df_features
