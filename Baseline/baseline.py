import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

def add_lag_features(data, columns, lags):
    for col in columns:
        for lag in range(1, lags + 1):
            data[f"{col}_lag{lag}"] = data[col].shift(lag)
    return data

def create_target_variable(data):
    data["Target"] = np.where(data["Close"].shift(-1) > data["Close"], 1, 0)
    return data

data = pd.read_csv("all_tickers_stock_data_with_sentiment_1.csv")
data.sort_values(by=["Ticker", "Date"], inplace=True)
columns_to_lag = ["Close", "Sentiment_tweet", "Sentiment_news"]
data = add_lag_features(data, columns_to_lag, lags=3)
data = create_target_variable(data)
data.dropna(inplace=True)

data = data.groupby("Ticker").filter(lambda x: len(x) > 1)

feature_columns = [col for col in data.columns if "lag" in col]
X = data[feature_columns]
y = data["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
rf = RandomForestClassifier(random_state=42, n_estimators=100)
rf.fit(X_train, y_train)

with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(rf, file)

X_test.to_csv("test_data.csv", index=False)

y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_rep)
print("Confusion Matrix:")
print(conf_matrix)
