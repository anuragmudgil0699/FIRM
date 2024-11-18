import json
import os
import time
from datetime import datetime

from constants import START_DATE, PREDICTION_RANGE, USER
from predictions import predict_stock_price_movement
from generate_stock_price import get_stock_price_data
from utils import get_all_tickers, get_date_time_object_from_string, get_string_from_date_time_object, get_next_date, get_previous_date


def get_ground_truth_prediction(ticker, date):

    today_price = get_stock_price_data(ticker, date)
    if today_price is None:
        return None
    while True:
        date = get_previous_date(date)
        prev_day_price = get_stock_price_data(ticker, date)
        if prev_day_price is not None:
            break
    return int(today_price > prev_day_price)

def test():

    results = []
    tickers = get_all_tickers()
    correct, wrong = 0, 0
    tp, tn, fp, fn = 0, 0, 0, 0
    start_date = get_date_time_object_from_string(START_DATE)
    interval = int(PREDICTION_RANGE)

    while interval > 0:
        for ticker in tickers:
            if 'BRK_A' in ticker:
                continue 
            print(ticker, start_date)
            ground_truth_prediction = get_ground_truth_prediction(ticker, start_date)
            if ground_truth_prediction is None:
                continue
            prediction, probability = predict_stock_price_movement(ticker, start_date)
            if prediction ==  ground_truth_prediction:
                if ground_truth_prediction == 1:
                    tp += 1
                else:
                    tn += 1
                correct += 1
            else:
                if ground_truth_prediction == 1:
                    fp += 1
                else:
                    fn += 1
                wrong += 1
            results.append({
                'ticker': ticker,
                'date': get_string_from_date_time_object(start_date), 
                'prediction': prediction, 
                'probability': probability, 
                'ground_truth_prediction': ground_truth_prediction
            })
            print(f'Accuracy: {correct / (correct + wrong)}')
        start_date = get_next_date(start_date)
        interval -= 1
        if interval > 0:
            time.sleep(20)
    accuracy = correct / (correct + wrong)
    results.insert(0, {'Accuracy': accuracy, 'True Positive': tp, 'True Negative': tn, 'False Positive': fp, 'False Negative': fn})
    return results

results = test()
current_time_str = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
path = f'Results/{USER}/{current_time_str}.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w') as json_file:
    json.dump(results, json_file, indent=4)
print(f"Results have been saved to {path}")
