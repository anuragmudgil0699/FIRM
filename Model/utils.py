import csv
import os
from constants import COMPANY_COUNT
from datetime import datetime, timedelta
import re

def get_all_tickers():
    file_path = os.path.join('.', 'Dataset/tickers.csv')
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tickers = [row['Company Ticker'] for row in reader]
    return tickers[:COMPANY_COUNT]

def get_previous_date(date_obj):
    return date_obj + timedelta(days=-1)

def get_n_prev_date(date_obj, n):
    return date_obj + timedelta(days=-1*n)

def get_next_date(date_obj):
    return date_obj + timedelta(days=1)

def get_date_time_object_from_string(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def get_string_from_date_time_object(date):
    return date.strftime("%Y-%m-%d")


def clean_tweets(tweets):
    # Remove hyperlinks
    cleaned_tweets = []
    for tweet in tweets:
        tweet = re.sub(r"http\S+|www.\S+", "", tweet)

        # Remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            "\U0001F700-\U0001F77F"  # Alchemical Symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols & Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols & Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed Characters
            "]+",
            flags=re.UNICODE,
        )
        tweet = emoji_pattern.sub(r"", tweet)

        # Remove hashtags but keep ticker symbols (words starting with $)
        tweet = re.sub(r"#\S+", "", tweet)

        # Remove unnecessary whitespace and line breaks
        tweet = re.sub(r"\s+", " ", tweet).strip()
        cleaned_tweets.append(tweet)
    return cleaned_tweets

