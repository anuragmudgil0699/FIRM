RELEVANT_TWEETS_PROMPT = """
You are a financial analyst. I will be sharing with you a list of tweets related to {company_name}. 
I need you to choose the most relevant tweets that you believe can provide insights into the company's 
performance and its impact on stock market value. 

Be very cautious when selecting the most relevant tweets, ensuring they are likely to provide indicators 
of the company's future stock market performance.

Data: {data}

Return only the top tweets in the following JSON format:
[{{ "text": string }}]

"""

RELEVANT_NEWS_PROMPT = """
You are a financial analyst. I will be sharing with you a list of 
Newspaper headlines for {company_name}. I need you to choose the most relevant newspaper headlines which you believe can negatively or positively impact the company's value. 
Be very cautious while choosing the most relevant articles (limit it to a maximum of 20 articles) such that you are confident they will actually impact values 
without being so vague as to cause false alarms. 

Data: {data}

Return only the top articles in the following JSON format:
{{\"news\": [{{ \"headline\": string, \"summary\": string}}]}}

"""

STOCK_PREDICTION_PROMPT = """
You are a financial analyst. Based on the given datasets which include newspaper headlines, tweets and the stock market price history of company {company_name}
We need you to give a prediction whether the stock market price of company {company_name} will either increase or decrease. 
Return prediction as 0 if you forcast stock price will decrease and 1 if you forcast stock price will increase along with probability.
Probability must be an integer from 0 to 100 representing the percentage probability of the forecast
INPUT:
News Data: {news_response.text}
Tweets: {tweet_response.text}
Stock Market History: {stock_history_data}

OUTPUT:
prediction, probability

SAMPLE OUTPUT:
If you think stock price will decrease with a probability of 75 return
OUTPUT: 0, 75
DO NOT GIVE ANY EXPLANATION
"""

FINAL_PROMPT = """

    You are a financial analyst tasked with predicting whether a company's stock price will rise tomorrow, based on the provided company name. 
    Follow the given set of instructions carefully to make your final prediction.
    
    Company Name: {company_name}
    Today's date: {date}
    
    We have retrieved the following information for this question:
    {retrieved_info}

    Instructions:
    1. Given the above problem statement, rephrase and expand it to help you do better answering. Maintain all
    information in the original question.
    {{ Insert rephrased and expanded question. }}
    2. Using your knowledge of the world and topic, as well as the information provided, provide a few
    reasons why the answer might be a no. Rate the strength of each reason.
    {{ Insert your thoughts }}
    3. Using your knowledge of the world and topic, as well as the information provided, provide a few
    reasons why the answer might be yes. Rate the strength of each reason.
    {{ Insert your thoughts }}
    4. Aggregate your considerations. Think like a superforecaster (e.g. Nate Silver).
    {{ Insert your aggregated considerations }}
    5. Output an initial probability (prediction) given steps 1-4.
    {{ Insert initial probability }}
    6. Evaluate whether your calculated probability is excessively confident or not confident enough. Also,
    consider anything else that might affect the forecast that you did not before consider (e.g. base rate of
    the event).
    {{ Insert your thoughts }}
    7. Output your final prediction (a number between 0 and 1) with an asterisk at the beginning and end
    of the decimal.
    {{ Insert your answer }}

"""


Tweet_QnA_Prompts = """ 
You are an AI assistant specializing in financial analysis. Given the following tweets about {company_name} collected on {date} and the 
data with which you are going to work with {data}, perform the following tasks:

1. **Relevance Filtering:** Identify and extract tweets that contain information likely to impact {company_name}'s stock price. Focus on tweets mentioning:
   - Company earnings or financial reports
   - Product launches or updates
   - Legal issues or lawsuits
   - Management or leadership changes
   - Significant market trends or events affecting the industry
   - Regulatory changes or government actions
   - Government Policies affecting the company

2. **Summarization:** Summarize the key points from the relevant tweets in a concise manner. Ensure that each summary point does not overlap or talk about the same subject.
    
3. **Question Generation:** Create insightful question-answer pairs based on the summarized information. Ensure that:
   - Each question targets a specific piece of important information.
   - Each answer is accurate and derived from the tweets.
   - Irrelevant or speculative content is excluded.

Please present the output in the following format:
"
    Summary points: 
    - {{summary point 1}}
    - {{summary point 2}}
    - {{summary point 3}}
    ...

  
    QnA Pairs: [
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 1",
            "answer": "Your Summary point 1"
        }},
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 2",
            "answer": "Your Summary point 2"
        }},
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 3",
            "answer": "Your Summary point 3"
        }}
    ]

"  
"""

New_QnA_prompt = """ 
You are an AI assistant specializing in financial analysis. Given the following news headlines and snippets about {company_name} collected on {date} and 
the data with which you are going to work with {data}, perform the following tasks:

1. **Relevance Filtering:** Identify and extract news items that contain information likely to impact {company_name}'s stock price. Focus on news mentioning:
   - Quarterly or annual earnings reports
   - Major product launches or failures
   - Mergers, acquisitions, or partnerships
   - Legal actions involving the company
   - Executive leadership changes
   - Industry-wide events affecting the company
   - Regulatory decisions or policy changes

2. **Summarization:** Summarize the key points from the relevant news items in a concise manner. Ensure that each summary point does not overlap or talk about the same subject.

3. **Question Generation:** Create insightful question-answer pairs based on the summarized information. Ensure that:
   - Each question targets a specific piece of important information.
   - Each answer is accurate and derived from the news content.
   - Irrelevant or speculative content is excluded.

Please present the output in the following format:
"
    Summary points: 
    - {{summary point 1}}
    - {{summary point 2}}
    - {{summary point 3}}
    ...

  
    QnA Pairs: [
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 1",
            "answer": "Your Summary point 1"
        }},
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 2",
            "answer": "Your Summary point 2"
        }},
        {{
            "question": "A question you have created that is relevant to stock market prediction which is answered by your summary point 3",
            "answer": "Your Summary point 3"
        }}
    ]

"  
"""
