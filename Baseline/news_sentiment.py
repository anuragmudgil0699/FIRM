import time
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import requests

sia = SentimentIntensityAnalyzer()

def calculate_sentiment(text):
    return sia.polarity_scores(text)["compound"]

def fetch_news_and_sentiment(tickers, start_date, end_date, source, finnhub_api_key, polygon_api_key):
    all_sentiment_data = []
    api_calls_finnhub = 0
    api_calls_polygon = 0

    for ticker in tickers:
        news = []
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')

        if source in ["finnhub", "both"]:
            finnhub_url = "https://finnhub.io/api/v1/company-news"
            finnhub_params = {
                "symbol": ticker,
                "from": from_date,
                "to": to_date,
                "token": finnhub_api_key
            }
            response_finnhub = requests.get(finnhub_url, params=finnhub_params)
            if response_finnhub.status_code == 200:
                finnhub_data = response_finnhub.json()
                for article in finnhub_data:
                    news.append({
                        "Ticker": ticker,
                        "Date": datetime.utcfromtimestamp(article.get("datetime", 0)).strftime('%Y-%m-%d'),
                        "Sentiment_news": calculate_sentiment(article.get("headline", "") + " " + article.get("summary", ""))
                    })
            api_calls_finnhub += 1

        if source in ["polygon", "both"]:
            polygon_url = "https://api.polygon.io/v2/reference/news"
            polygon_params = {
                "ticker": ticker,
                "published_utc.gte": from_date,
                "published_utc.lte": to_date,
                "apiKey": polygon_api_key
            }
            response_polygon = requests.get(polygon_url, params=polygon_params)
            if response_polygon.status_code == 200:
                polygon_data = response_polygon.json().get("results", [])
                for article in polygon_data:
                    news.append({
                        "Ticker": ticker,
                        "Date": article.get("published_utc", "").split("T")[0],
                        "Sentiment_news": calculate_sentiment(article.get("title", "") + " " + article.get("description", ""))
                    })
            api_calls_polygon += 1

        if api_calls_finnhub >= 5 or api_calls_polygon >= 5:
            time.sleep(60)
            api_calls_finnhub = 0
            api_calls_polygon = 0

        all_sentiment_data.extend(news)

    sentiment_df = pd.DataFrame(all_sentiment_data)
    sentiment_aggregated = sentiment_df.groupby(["Ticker", "Date"]).agg({"Sentiment_news": "mean"}).reset_index()
    return sentiment_aggregated

def merge_sentiment_with_stock_data(stock_data_file, tickers, start_date, end_date, source, output_file, finnhub_api_key, polygon_api_key):
    sentiment_data = fetch_news_and_sentiment(tickers, start_date, end_date, source, finnhub_api_key, polygon_api_key)
    stock_data = pd.read_csv(stock_data_file)
    stock_data["Date"] = pd.to_datetime(stock_data["Date"]).dt.strftime('%Y-%m-%d')
    merged_data = pd.merge(stock_data, sentiment_data, on=["Ticker", "Date"], how="left")
    merged_data.to_csv(output_file, index=False)

tickers_file_path = "../Dataset/tickers.csv"
tickers_df = pd.read_csv(tickers_file_path)
tickers = tickers_df['Company Ticker'].str.strip().tolist()

start_date = datetime.strptime("2024-08-06", "%Y-%m-%d")
end_date = datetime.strptime("2024-08-14", "%Y-%m-%d")
source = "both"
finnhub_api_key = "cn8ooc1r01qocbpgs9h0cn8ooc1r01qocbpgs9hg"
polygon_api_key = "GdSGxrAOB7yW9hlw3Wym69h4MapsLye5"
stock_data_file = "all_tickers_stock_data_with_sentiment.csv"
output_file = "all_tickers_stock_data_with_sentiment_1.csv"

merge_sentiment_with_stock_data(stock_data_file, tickers, start_date, end_date, source, output_file, finnhub_api_key, polygon_api_key)
