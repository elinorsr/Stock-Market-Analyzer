"""
🚀 Trading Signal Bot - Main Execution Script

This script serves as the entry point for the trading bot.
It utilizes the core logic to generate buy/sell signals based on Fibonacci retracements
and visualizes the data for both Cryptocurrencies and Stock Market assets.

Author: Elinor Srur
"""

# Importing core logic from the modular package
from core.signal_generator import generate_fibonacci_signal
from core.plot_fibonacci import plot_fibonacci_chart

if __name__ == "__main__":
    print("🚀 Starting Trading Bot Analysis...\n")

    # --- 1. Cryptocurrency Analysis ---
    # Analyzing XRP/USDT pair using Binance exchange data
    print("🔍 XRPUSDT Analysis:")
    # Generates signal (Buy/Sell/Neutral) based on technical indicators
    print(generate_fibonacci_signal("XRPUSDT", "BINANCE"))

    # --- 2. Stock Market Analysis ---
    # Analyzing NASDAQ QQQ ETF using the American screener
    print("\n🔍 NASDAQ (QQQ) Analysis:")
    print(generate_fibonacci_signal("QQQ", "NASDAQ", screener="america"))

    # --- 3. Visualization ---
    # Plotting the Fibonacci charts for visual confirmation
    print("\n📊 Generating Charts...")
    plot_fibonacci_chart("XRP-USD")  # Plot Crypto chart
    plot_fibonacci_chart("QQQ")      # Plot Stock chart

    print("\n✅ Analysis Complete.")