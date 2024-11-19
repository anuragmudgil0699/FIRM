import os
import json
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

def analyze_tweet_sentiment(tweet_text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(tweet_text)["compound"]

def process_tweet_data(tweet_folder, start_date, end_date, ticker_mapping):
    sentiment_data = []
    for filename in os.listdir(tweet_folder):
        if filename.endswith(".json"):
            company_name = filename.replace(".json", "").strip().split()[0]  # Use only the first word
            ticker = ticker_mapping.get(company_name)
            if not ticker:
                continue
            file_path = os.path.join(tweet_folder, filename)
            with open(file_path, "r") as f:
                tweets = json.load(f)
                for date, daily_tweets in tweets.items():
                    if start_date <= date <= end_date:
                        daily_sentiments = [
                            analyze_tweet_sentiment(tweet["text"]) for tweet in daily_tweets
                        ]
                        if daily_sentiments:
                            avg_sentiment = sum(daily_sentiments) / len(daily_sentiments)
                            sentiment_data.append({"Ticker": ticker, "Date": date, "Sentiment_tweet": avg_sentiment})
    sentiment_df = pd.DataFrame(sentiment_data)
    return sentiment_df

def merge_with_stock_data(stock_data_file, sentiment_data, output_file):
    stock_data = pd.read_csv(stock_data_file)
    stock_data["Date"] = pd.to_datetime(stock_data["Date"]).dt.strftime('%Y-%m-%d')
    stock_data["Ticker"] = stock_data["Ticker"].str.split().str[0].str.strip().str.upper()
    sentiment_data["Date"] = pd.to_datetime(sentiment_data["Date"]).dt.strftime('%Y-%m-%d')
    sentiment_data["Ticker"] = sentiment_data["Ticker"].str.split().str[0].str.strip().str.upper()
    merged_data = pd.merge(stock_data, sentiment_data, on=["Ticker", "Date"], how="left")
    print("Merged Data Preview:")
    print(merged_data.head())
    merged_data.to_csv(output_file, index=False)
    print(f"Updated data saved to {output_file}")

tweet_folder = "../Dataset/Tweets"
stock_data_file = "all_tickers_stock_data.csv"
output_file = "all_tickers_stock_data_with_sentiment.csv"
start_date = "2024-08-06"
end_date = "2024-08-14"

ticker_mapping_df = pd.read_csv("../Dataset/tickers.csv")
ticker_mapping_df["Truncated_Company"] = ticker_mapping_df["Company Name"].str.split().str[0]
ticker_mapping_df["Truncated_Ticker"] = ticker_mapping_df["Company Ticker"].str.split().str[0].str.lower()
ticker_mapping = dict(zip(ticker_mapping_df["Truncated_Company"], ticker_mapping_df["Truncated_Ticker"]))

sentiment_data = process_tweet_data(tweet_folder, start_date, end_date, ticker_mapping)
print("Processed Sentiment Data:")
print(sentiment_data.head())
merge_with_stock_data(stock_data_file, sentiment_data, output_file)
