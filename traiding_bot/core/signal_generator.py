from tradingview_ta import TA_Handler
from core.fibonacci_utils import calculate_fibonacci_levels

def get_price_range(symbol: str, exchange: str, screener: str = "crypto") -> tuple:
    """
    Fetches the High and Low prices for a given symbol over a specified timeframe.
    Currently uses '1h' interval to determine Swing High/Low points.

    Args:
        symbol (str): Ticker symbol (e.g., 'BTCUSDT').
        exchange (str): Exchange name (e.g., 'BINANCE').
        screener (str): Market screener (default: 'crypto').

    Returns:
        tuple: (high, low) as floats, or (None, None) if an error occurs.
    """
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval="1h"  # Using 1-hour candles to identify significant levels
        )
        analysis = handler.get_analysis()
        return analysis.indicators['high'], analysis.indicators['low']
    except Exception as e:
        print(f"❌ Error fetching price range for {symbol}: {e}")
        return None, None

def generate_fibonacci_signal(symbol: str, exchange: str, screener: str = "crypto") -> str:
    """
    Analyzes the current price position relative to calculated Fibonacci levels.

    It performs a Multi-Timeframe Analysis:
    1. Calculates levels based on '1h' timeframe (Macro view).
    2. Compares current price from '1m' timeframe (Micro view).
    
    Returns:
        str: A formatted message indicating if the price is near a key level.
    """
    # 1. Get Macro Levels (Swing High/Low)
    high, low = get_price_range(symbol, exchange, screener)
    
    if high is None or low is None:
        return "⚠️ Error: Could not retrieve price data."

    levels = calculate_fibonacci_levels(high, low)

    try:
        # 2. Get Current Micro Price (Real-time execution price)
        current_price = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval="1m"
        ).get_analysis().indicators['close']

        # 3. Check for Proximity (Signal Logic)
        # We define a 'tolerance' threshold of 0.3% (0.003) around the level
        # to account for market noise.
        tolerance_ratio = 0.003 

        for label, level in levels.items():
            if abs(current_price - level) < (tolerance_ratio * current_price):
                return f"⚠️ Close to Fibonacci level {label} at {level:.4f} (Current: {current_price:.4f})"
        
        return f"✅ No significant Fibonacci level nearby. (Current: {current_price:.4f})"

    except Exception as e:
        return f"⚠️ Error analyzing signal: {str(e)}"