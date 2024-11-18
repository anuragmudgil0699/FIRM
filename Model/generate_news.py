import requests
from constants import FINNHUB_API_KEY, POLYGON_API_KEY, NEWS_RANGE
from utils import get_n_prev_date, get_previous_date, get_string_from_date_time_object, get_date_time_object_from_string

def get_news(ticker, date, source):

    news = []
    start_date = get_previous_date(date)
    end_date = get_n_prev_date(date, NEWS_RANGE)
    
    from_date = get_string_from_date_time_object(end_date)
    to_date = get_string_from_date_time_object(start_date)

    # Finnhub API
    if source in ["finnhub", "both"]:
        finnhub_url = "https://finnhub.io/api/v1/company-news"
        finnhub_params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": FINNHUB_API_KEY
        }
        
        response_finnhub = requests.get(finnhub_url, params=finnhub_params)
        
        if response_finnhub.status_code == 200:
            finnhub_data = response_finnhub.json()
            for article in finnhub_data:
                news.append({
                    "headline": article["headline"],
                    "summary": article["summary"]
                })
        else:
            print(f"Failed to retrieve Finnhub data. Status code: {response_finnhub.status_code}")
    
    # Polygon API
    if source in ["polygon", "both"]:
        polygon_url = "https://api.polygon.io/v2/reference/news"
        polygon_params = {
            "ticker": ticker,
            "published_utc.gte": from_date,
            "published_utc.lte": to_date,
            "apiKey": POLYGON_API_KEY
        }
        
        response_polygon = requests.get(polygon_url, params=polygon_params)
        
        if response_polygon.status_code == 200:
            polygon_data = response_polygon.json().get("results", [])
            for article in polygon_data:
                news.append({
                    "headline": article["title"],
                    "summary": article["description"]
                })
        else:
            print(f"Failed to retrieve Polygon data. Status code: {response_polygon.status_code}")
    
    return news


# news_articles = get_news(
#     ticker="AAPL",
#     date=get_date_time_object_from_string("2024-08-15"),
#     source="polygon"
# )

# for article in news_articles:
#     print(f"Headline: {article['headline']}\nSummary: {article['summary']}\n")
