# ml/model_loader.py
import joblib
import pandas as pd
from core.fibonacci_utils import calculate_fibonacci_levels

model = joblib.load("ml/fibo_model.pkl")

def extract_features_for_prediction(latest_df):
    high = latest_df["High"].max()
    low = latest_df["Low"].min()
    fibo_levels = calculate_fibonacci_levels(high, low)

    price_diff = latest_df["Close"].iloc[-1] - latest_df["Close"].iloc[-2]
    above_0_618 = latest_df["Close"].iloc[-1] > fibo_levels["0.618"]

    return pd.DataFrame([[price_diff, above_0_618]], columns=["price_diff", "above_0.618"])

def predict_fibo_signal(latest_df):
    features = extract_features_for_prediction(latest_df)
    prediction = model.predict(features)[0]
    return "📈 AI predicts rise" if prediction == 1 else "📉 AI predicts no rise"
