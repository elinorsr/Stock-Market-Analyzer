import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core.fibonacci_utils import calculate_fibonacci_levels

class StockPlotter:
    """
    Handles fetching and visualization of Stock Market data (e.g., NASDAQ, NYSE).
    Uses 'yfinance' API to retrieve historical data and overlays Fibonacci levels.
    """

    def __init__(self, symbol='NANO', period='1mo', interval='1h'):
        """
        Initializes the StockPlotter.

        Args:
            symbol (str): The stock ticker symbol (e.g., 'AAPL', 'QQQ').
            period (str): The historical period to download (e.g., '1mo', '1y').
            interval (str): The data resolution (e.g., '1h', '1d').
        """
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def fetch_data(self) -> pd.DataFrame:
        """
        Fetches historical market data using Yahoo Finance API.
        
        Returns:
            pd.DataFrame: A DataFrame containing OHLC data with a standardized 'Datetime' column.
        """
        try:
            ticker = yf.Ticker(self.symbol)
            df = ticker.history(period=self.period, interval=self.interval)
            
            # Reset index to make 'Date'/'Datetime' a column instead of index
            df.reset_index(inplace=True)

            # 🛠️ Fix: Standardize Date Column Name
            # yfinance returns 'Date' for daily data and 'Datetime' for intraday.
            # We rename it to 'Datetime' for consistency across the app.
            if 'Date' in df.columns:
                df.rename(columns={'Date': 'Datetime'}, inplace=True)
            
            return df
        except Exception as e:
            st.error(f"❌ Error fetching data for {self.symbol}: {e}")
            return pd.DataFrame()

    def plot(self):
        """
        Renders an interactive Candlestick chart in Streamlit with Fibonacci overlays.
        """
        data = self.fetch_data()

        # 1. Validation: Check if data exists
        if data.empty:
            st.warning(f"⚠️ No data found for symbol: {self.symbol}")
            return

        # 2. Validation: Check for required columns
        if 'Datetime' not in data.columns:
            st.error("⚠️ Data Error: Missing 'Datetime' column.")
            return

        # --- Fibonacci Calculation ---
        high = data['High'].max()
        low = data['Low'].min()
        levels = calculate_fibonacci_levels(high, low)

        # --- Chart Construction ---
        fig = go.Figure(data=[go.Candlestick(
            x=data['Datetime'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=self.symbol
        )])

        # Draw Fibonacci Lines
        for label, level in levels.items():
            fig.add_hline(
                y=float(level), 
                line_dash="dash", 
                annotation_text=label, 
                line_color="blue",
                annotation_position="top right"
            )

        # Update layout for better visibility
        fig.update_layout(
            title=f"📈 Stock Analysis: {self.symbol} ({self.interval})",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)