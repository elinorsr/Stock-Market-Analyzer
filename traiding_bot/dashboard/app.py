"""
📊 FiboBot Streamlit Dashboard

This application serves as the user interface for the FiboBot trading system.
It provides real-time visualization of Fibonacci levels, technical analysis signals,
and AI-based trend predictions for both Cryptocurrencies and Stock Market assets.

Author: Elinor Srur
Framework: Streamlit
"""

import sys
import os
import streamlit as st

# --- Path Setup ---
# Add the parent directory to sys.path to allow importing from 'core' and 'ml' modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Module Imports ---
from core.stock_plotter import StockPlotter
from ml.model_loader import predict_fibo_signal
from core.signal_generator import generate_fibonacci_signal
from core.plot_fibonacci import FibonacciPlotter

# --- Streamlit Configuration ---
st.set_page_config(page_title="📊 FiboBot Dashboard", layout="wide")
st.title("📉 Real-Time Fibonacci Dashboard")

# Define supported assets with their corresponding symbols, exchanges, and screener types
assets = {
    "XRP (XRP/USDT)": ("XRPUSDT", "BINANCE", "crypto"),
    "NASDAQ 100 (QQQ)": ("QQQ", "NASDAQ", "america")
}

# --- Caching Mechanism ---
# Caches the signal generation to prevent excessive API calls and improve performance.
# Data is refreshed every 600 seconds (10 minutes).
@st.cache_data(ttl=600)
def get_signal(symbol, exchange, screener):
    return generate_fibonacci_signal(symbol, exchange, screener)

# --- Main Dashboard Loop ---
# Iterate through each asset to display its section
for name, (symbol, exchange, screener) in assets.items():
    st.subheader(name)

    # Fetch and display the technical signal (Buy/Sell/Neutral)
    # Note: Removing dashes from symbol for compatibility with the signal generator
    signal = get_signal(symbol.replace("-", ""), exchange, screener)
    st.text(signal)

    # --- User Controls (Expander) ---
    with st.expander(f"⚙️ הגדרות תצוגת גרף ל-{name}"):
        # Allow user to select time period and interval resolution
        period = st.selectbox(f"⏳ תקופה עבור {name}", ["7d", "1mo", "3mo", "6mo"], key=f"{symbol}_period")
        interval = st.selectbox(f"📅 רזולוציה עבור {name}", ["1h", "1d", "1wk"], key=f"{symbol}_interval")

        # --- Plotting Logic ---
        if st.button(f"📈 הצג גרף פיבונאצ'י עבור {name}"):
            loading_text = f"📡 טוען גרף עבור {symbol} עם תקופה {period} ורזולוציה {interval}..."
            st.write(loading_text)

            df = None  # Initialize dataframe variable

            # 1. Handling Crypto Assets
            if screener == "crypto":
                # Using FibonacciPlotter for crypto assets (e.g., binance pairs)
                plotter = FibonacciPlotter(symbol=f"{symbol.replace('USDT', '/USDT')}", timeframe=interval)
                plotter.plot()
                df = plotter.fetch_data()

            # 2. Handling US Stocks
            elif screener == "america":
                # Using StockPlotter for US market assets (e.g., NASDAQ)
                plotter = StockPlotter(symbol=symbol, period=period, interval=interval)
                plotter.plot()
                df = plotter.fetch_data()

            else:
                st.error("❌ סוג נכס לא נתמך להצגת גרף")
                continue

            # --- AI Prediction Integration ---
            # If data is successfully fetched, run the ML model for prediction
            if df is not None and not df.empty:
                try:
                    ai_signal = predict_fibo_signal(df)
                    st.success(f"🤖 AI Signal: {ai_signal}")
                except Exception as e:
                    st.error(f"AI Prediction Error: {e}")
            else:
                st.warning("לא ניתן לבצע חיזוי – הדאטה ריק.")