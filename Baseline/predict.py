import pandas as pd
import pickle

with open("random_forest_model.pkl", "rb") as file:
    rf = pickle.load(file)

data = pd.read_csv("all_tickers_stock_data_with_sentiment_1.csv")
data.sort_values(by=["Ticker", "Date"], inplace=True)
columns_to_lag = ["Close", "Sentiment_tweet", "Sentiment_news"]

def add_lag_features(data, columns, lags):
    for col in columns:
        for lag in range(1, lags + 1):
            data[f"{col}_lag{lag}"] = data[col].shift(lag)
    return data

data = add_lag_features(data, columns_to_lag, lags=3)
data.dropna(inplace=True)  # Ensure we only use rows with valid lag features

# Select the most recent data (2024-08-14) for prediction
latest_date = "2024-08-14"
data_to_predict = data[data["Date"] == latest_date]

if data_to_predict.empty:
    print(f"No data available for prediction on {latest_date}. Ensure the dataset contains relevant historical data.")
else:
    feature_columns = [col for col in data.columns if "lag" in col]
    X_to_predict = data_to_predict[feature_columns]

    # Make predictions for 2024-08-15
    predictions = rf.predict(X_to_predict)

    data_to_predict["Prediction"] = predictions
    data_to_predict = data_to_predict[["Date", "Ticker", "Prediction"]]
    data_to_predict["Date"] = "2024-08-15"  # Update date to represent the prediction date
    print(data_to_predict)
    data_to_predict.to_csv("predictions_08_15.csv", index=False)
