from constants import STOCK_PRICES_RANGE
from generate_stock_price import get_stock_price_data_range, get_company_financials
from llm import call_llm
from prompts import SUMMARIZE_FINANCIAL_DATA_PROMPT
from utils import get_date_time_object_from_string

def get_question_answer_pairs(ticker, company, date):

    stock_price_last_days = get_stock_price_data_range(ticker, date, STOCK_PRICES_RANGE)
    company_financial = get_company_financials(stock_price_last_days)
    summarized_analysis = call_llm(SUMMARIZE_FINANCIAL_DATA_PROMPT.format(historical_data=stock_price_last_days, stock_market_features=company_financial))
    summarized_analysis = summarized_analysis.text
    result = [
        {
            'question': f'What is the stock price of {company} for the last {STOCK_PRICES_RANGE} days',
            'answer':  stock_price_last_days
        },
        {
            'question': f'What are the financials of the stock price of {company} for the last {STOCK_PRICES_RANGE} days',
            'answer': company_financial
        },
        {
            'question': f'Summarize the stock movement of {company} for the last {STOCK_PRICES_RANGE} days',
            'answer': f'{summarized_analysis}'
        }
    ]
    return result


print(get_question_answer_pairs('AAPL', 'Apple INC.', get_date_time_object_from_string('2024-08-15')))

