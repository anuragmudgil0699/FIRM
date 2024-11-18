import re
from generate_q_n_a_pairs import generate_QnA_pairs
from data_initializer import ticker_to_company_name
from llm import call_llm
from prompts import FINAL_PROMPT
from utils import get_date_time_object_from_string


def extract_prediction(text):
    start_index = text.find("Final Prediction:")
    if start_index != -1:
        relevant_text = text[start_index:]
        matches = re.findall(r"#(.*?)#", relevant_text)
        return float(matches[0])
    else:
        print("Final Prediction not found.")

def predict_stock_price_movement(ticker, date):

    company_name = ticker_to_company_name.get(ticker)
    qa_pair = generate_QnA_pairs(company_name, ticker, date)
    prompt = FINAL_PROMPT.format(company_name=company_name, date=date, retrieved_info=qa_pair)
    response = call_llm(prompt=prompt)
    print(f"RESPONSE!!!!!!!!!!!!! :\n {response}")
    prediction = extract_prediction(response)
    if prediction < 0.5:
        return 0, prediction
    return 1, prediction

#print(predict_stock_price_movement('AAPL', '2024-08-15'))