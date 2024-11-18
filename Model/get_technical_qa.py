from constants import STOCK_PRICES_RANGE
from generate_stock_price import get_stock_price_data_range
from utils import get_date_time_object_from_string




def get_question_answer_pairs(ticker, company, date):

    stock_price_last_days = get_stock_price_data_range(ticker, get_date_time_object_from_string(date), STOCK_PRICES_RANGE)
    summarized_analysis = ''
    prediction = ''
    result = {
        f'What is the stock price of {company} for the last {STOCK_PRICES_RANGE} days': stock_price_last_days, 
        f'Summarize the stock movement of {company} for the last {STOCK_PRICES_RANGE} days': summarized_analysis, 
        f'What does simple machine learning models predict using this data for the {STOCK_PRICES_RANGE} few days': prediction
    }
    print(result)


get_question_answer_pairs('AAPL', 'Apple INC.', '2024-08-15')

