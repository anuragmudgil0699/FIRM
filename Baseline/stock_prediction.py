import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def get_previous_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    previous_date = date_obj - timedelta(days=1)
    return previous_date.strftime("%Y-%m-%d")

def get_next_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date_obj + timedelta(days=1)
    return next_date.strftime("%Y-%m-%d")

def get_company_financials(ticker, date):
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=date, end=get_next_date(date))
    if historical_data.empty:
        return None
    return historical_data

def fetch_and_process_stock_data(ticker, start_date, end_date):
    all_data = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        stock_data = get_company_financials(ticker, current_date)
        if stock_data is not None:
            all_data = pd.concat([all_data, stock_data])
        current_date = get_next_date(current_date)
    if not all_data.empty:
        all_data.reset_index(inplace=True)
        all_data['Date'] = pd.to_datetime(all_data['Date']).dt.strftime('%Y-%m-%d') 
        all_data = all_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        date_range = pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d')
        all_data.set_index('Date', inplace=True)
        all_data = all_data.reindex(date_range, method='ffill')
        all_data.reset_index(inplace=True)
        all_data.rename(columns={'index': 'Date'}, inplace=True)
    return all_data

tickers_file_path = "../Dataset/tickers.csv"
tickers_df = pd.read_csv(tickers_file_path)
print(tickers_df.head())
tickers = tickers_df['Company Ticker'].str.strip().tolist()

start_date = "2024-08-06"
end_date = "2024-08-14"
all_tickers_data = pd.DataFrame()

for ticker in tickers:
    ticker_data = fetch_and_process_stock_data(ticker, start_date, end_date)
    if not ticker_data.empty:
        ticker_data['Ticker'] = ticker
        all_tickers_data = pd.concat([all_tickers_data, ticker_data], ignore_index=True)

print(all_tickers_data.head(20))
output_file_path = "all_tickers_stock_data.csv"
all_tickers_data.to_csv(output_file_path, index=False)
print(f"Data saved to {output_file_path}")