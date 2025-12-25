import ccxt
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from core.fibonacci_utils import calculate_fibonacci_levels

class FibonacciPlotter:
    """
    Handles the fetching, processing, and visualization of cryptocurrency data.
    It overlays Fibonacci retracement levels on a Candlestick chart and annotates
    potential Buy/Sell signals based on price breakouts.
    """

    def __init__(self, symbol='XRP/USDT', timeframe='1h', limit=100):
        """
        Initializes the plotter settings.

        Args:
            symbol (str): The trading pair (e.g., 'XRP/USDT').
            timeframe (str): Data resolution (e.g., '1h', '1d').
            limit (int): Number of candles to fetch.
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit

    def fetch_data(self) -> pd.DataFrame:
        """
        Connects to Binance API to retrieve historical OHLCV data.
        
        Returns:
            pd.DataFrame: A DataFrame containing Timestamp, Open, High, Low, Close, Volume.
        """
        try:
            exchange = ccxt.binance()
            # Fetching candles
            ohlcv = exchange.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=500)
            # Converting to DataFrame
            df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
            return df
        except Exception as e:
            st.error(f"Error fetching data from Binance: {e}")
            return pd.DataFrame()

    def plot(self):
        """
        Main method to render the interactive Plotly chart in Streamlit.
        Calculates Fibonacci levels and adds annotations for trade signals.
        """
        data = self.fetch_data()

        # Display raw data table for transparency
        st.subheader(f"📊 Raw Data for {self.symbol}")
        st.write(data.head(10))

        # Data Validation
        if data.empty:
            st.warning("⚠️ No data found!")
            return

        data = data.dropna(subset=["Open", "High", "Low", "Close"])
        if data.empty:
            st.warning("⚠️ Data is missing OHLC values!")
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
            name="Price"
        )])

        # Draw Fibonacci Lines
        for label, level in levels.items():
            fig.add_hline(y=float(level), line_dash="dash", annotation_text=label, line_color="blue")

        # --- Signal Logic: Breakout Detection ---
        # Iterating through history to find where price crossed a Fibonacci level
        for i in range(1, len(data)):
            current_price = data["Close"].iloc[i]
            previous_price = data["Close"].iloc[i - 1]
            time = data["Datetime"].iloc[i]

            for label, level_price in levels.items():
                # Detect Bullish Breakout (Crossing Up)
                if previous_price < level_price and current_price > level_price:
                    fig.add_annotation(
                        x=time, y=current_price,
                        text="BUY", showarrow=True, arrowhead=2, arrowsize=1,
                        arrowcolor="green", font=dict(color="green", size=10),
                        ax=0, ay=-30
                    )
                # Detect Bearish Breakout (Crossing Down)
                elif previous_price > level_price and current_price < level_price:
                    fig.add_annotation(
                        x=time, y=current_price,
                        text="SELL", showarrow=True, arrowhead=2, arrowsize=1,
                        arrowcolor="red", font=dict(color="red", size=10),
                        ax=0, ay=30
                    )

        # --- Custom Strategy Alerts (Hardcoded Levels) ---
        # Note: In a production environment, these levels should be dynamic parameters.
        for i in range(len(data)):
            price = data["Close"].iloc[i]
            time = data["Datetime"].iloc[i]

            if price > 3.30:
                fig.add_annotation(
                    x=time, y=price,
                    text="📈 ניסיון פריצה – שקול כניסה", # "Attempting Breakout - Consider Entry"
                    showarrow=True, arrowhead=2, arrowsize=1.5,
                    arrowcolor="green", font=dict(color="green", size=10),
                    ax=0, ay=-40,
                )
            elif price < 2.98:
                fig.add_annotation(
                    x=time, y=price,
                    text="⚠ מחיר מתחת 2.98 – צא או המתן", # "Price below 2.98 - Exit or Wait"
                    showarrow=True, arrowhead=2, arrowsize=1.5,
                    arrowcolor="red", font=dict(color="red", size=10),
                    ax=0, ay=40,
                )

        # Render the final chart
        st.plotly_chart(fig, use_container_width=True)