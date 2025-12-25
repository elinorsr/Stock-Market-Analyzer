# ml/trainer.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from core.fibonacci_utils import calculate_fibonacci_levels
import ccxt

def fetch_data(symbol='XRP/USDT', timeframe='1h', limit=500):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df

def build_features(df):
    high = df["High"].max()
    low = df["Low"].min()
    fibo_levels = calculate_fibonacci_levels(high, low)

    df["price_diff"] = df["Close"].diff()
    df["above_0.618"] = df["Close"] > fibo_levels["0.618"]
    df["target"] = df["Close"].shift(-3) > df["Close"]  # אם עולה תוך 3 צעדים

    features = df[["price_diff", "above_0.618"]].dropna().astype(float)
    labels = df["target"].dropna().astype(int)

    return features, labels[:len(features)]

def train_and_save_model():
    df = fetch_data()
    X, y = build_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, "ml/fibo_model.pkl")
    print("✅ Model trained and saved to ml/fibo_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
