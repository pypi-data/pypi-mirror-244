import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta
import json
from aerarium.consts import DATA_FILE_PATH


def load_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    data = [entry for entry in data if entry["type"] == "withdraw"]
    return pd.DataFrame(data)


def preprocess_data(df):
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    return df


def train_model(df, features, target):
    train_size = int(len(df) * 0.8)
    train_data, test_data = df[:train_size], df[train_size:]

    X_train, y_train = train_data[features], train_data[target]
    X_test, y_test = test_data[features], test_data[target]

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae


def predict_spending(model, n_days, current_date):
    future_dates = [current_date + timedelta(days=i) for i in range(n_days)]
    future_data = pd.DataFrame(
        {
            "day_of_week": [date.weekday() for date in future_dates],
            "month": [date.month for date in future_dates],
        }
    )
    future_predictions = model.predict(future_data)
    return sum(future_predictions)


def predict_spending_for_n_days(n_days):
    data = load_data(DATA_FILE_PATH)
    df = preprocess_data(data)

    features = ["day_of_week", "month"]
    target = "amount"

    model, _, _ = train_model(df, features, target)

    current_date = datetime.now()
    predicted_spending = predict_spending(model, n_days, current_date)

    print(f"Predicted Spending for the next {n_days} day(s): {predicted_spending:.2f}")


if __name__ == "__main__":
    file_path = "../tests/data/transactions.json"
    df = load_data(file_path)
    df = preprocess_data(df)

    features = ["day_of_week", "month"]
    target = "amount"

    model, X_test, y_test = train_model(df, features, target)
    mae = evaluate_model(model, X_test, y_test)
    print(f"Mean Absolute Error: {mae}")

    n_days_to_predict = 3
    current_date = datetime.now()
    predicted_spending = predict_spending(model, n_days_to_predict, current_date)
    print(
        f"Predicted Spending for the next {n_days_to_predict} days: {predicted_spending}"
    )
