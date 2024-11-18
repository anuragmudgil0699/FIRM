from data_initializer import ticker_to_company_name
from predictions import call_llm
from prompts import FINAL_PROMPT

def get_question_answer_pair(ticker, date):
    return [{
        'question': 'Has there been significant stock trade for apple?',
        'answer': 'What Does Warren Buffett Know That We Don t?\n\nThe billionaire investor has just offloaded a jaw-dropping $77 billion in stocks in the second quarter alone\u2014a figure that dwarfs his typical annual sales.\n\nWhat does it signal for the economy?\n\nThis is \"the biggest warning yet that'
    }]

def predict_stock_price_movement(ticker, date):

    company_name = ticker_to_company_name.get(ticker)
    qa_pair = get_question_answer_pair(ticker, date)
    prompt = FINAL_PROMPT.format(company_name=company_name, date=date, retrieved_info=qa_pair)
    response = call_llm(prompt=prompt)
    print(response.text)
    

predict_stock_price_movement('AAPL', '2024-08-15')