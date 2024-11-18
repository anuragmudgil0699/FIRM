import re
from prompts import Tweet_QnA_Prompts, New_QnA_prompt
from llm import call_llm
from generate_news import get_news
import json
from utils import clean_tweets
from generate_twitter_data import get_tweets

def extract_qna_pairs(text):
    qna_start = text.find("QnA Pairs")
    if qna_start == -1:
        raise ValueError("QnA Pairs section not found in the input string.")

    # Extract everything after "QnA Pairs:"
    qna_content = text[qna_start + len("QnA Pairs:"):].strip()

    # Use regex to find the JSON array within the text
    match = re.search(r'\[\s*{.*}\s*\]', qna_content, re.DOTALL)
    if not match:
        raise ValueError("QnA pairs section does not contain a valid JSON array.")

    json_str = match.group(0)

    # Parse the JSON content
    try:
        qna_pairs = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding QnA JSON content: {e}")

    return qna_pairs


def news_concatenate(news):
    concatenated_paragraph = []

    for article in news:
        if not isinstance(article, dict):
            continue

        headline = article.get("headline", "").strip()
        summary = article.get("summary", "").strip()

        # Only add if both headline and summary are non-empty
        # if headline and summary:
        concatenated_paragraph.append(f"{headline}: {summary}")

    # Join all sentences into a single paragraph
    return " ".join(concatenated_paragraph)


def tweet_concatenate(tweets):
    return " ".join(tweets)


def Tweet_QnA(company_name, date, data):
    prompt = Tweet_QnA_Prompts.format(company_name=company_name, date=date, data=data)
    tweet_response = call_llm(prompt)
    print(tweet_response.text)
    Q_n_A = extract_qna_pairs(tweet_response.text)
    print("Tweet LIST!!!")
    print(Q_n_A)
    return Q_n_A


def News_QnA(company_name, date, data):
    prompt = New_QnA_prompt.format(company_name=company_name, date=date, data=data)
    news_response = call_llm(prompt)
    print(news_response.text)
    Q_n_A = extract_qna_pairs(news_response.text)
    print("NEWS LIST!!!")
    print(Q_n_A)
    return Q_n_A


def generate_QnA_pairs(company_name, ticker, date): #I am under the impression that date here is a date time object
    date_str = date.strftime("%Y-%m-%d")
    # This is tweet call
    tweet_scrap = get_tweets(ticker, date=date) 
    cleaned_tweets = clean_tweets(tweet_scrap)
    tweet_para = tweet_concatenate(cleaned_tweets)
    tweet_qna = Tweet_QnA(company_name, date_str, tweet_para) #[{'question': "How diment?", 'answer': "Warr ...."} , {'question': "How diment?", 'answer': "Warr ...."}]
    # This is News call
    news_articles = get_news(ticker=ticker, date=date, source="both")
    news_paragraph = news_concatenate(news_articles)
    news_qna = News_QnA(company_name, date_str, news_paragraph)

    return tweet_qna + news_qna
