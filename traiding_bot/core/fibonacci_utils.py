def calculate_fibonacci_levels(high: float, low: float) -> dict:
    """
    Calculates standard Fibonacci retracement levels for a given price range.

    This function computes key support and resistance levels used in technical analysis
    by applying standard Fibonacci ratios to the difference between the high and low prices.

    Args:
        high (float): The highest price in the selected period (Swing High).
        low (float): The lowest price in the selected period (Swing Low).

    Returns:
        dict: A dictionary mapping Fibonacci percentages (e.g., '61.8%') to their calculated price levels.
    """
    
    # Calculate the vertical price range (Swing High - Swing Low)
    diff = high - low

    # Compute retracement levels by subtracting the ratio portion from the high
    levels = {
        "0.0%": high,                    # The Peak (Resistance)
        "23.6%": high - 0.236 * diff,    # Shallow retracement
        "38.2%": high - 0.382 * diff,    # Moderate support level
        "50.0%": high - 0.5 * diff,      # Psychological level (Market midpoint)
        "61.8%": high - 0.618 * diff,    # The "Golden Ratio" - Key support/resistance level
        "78.6%": high - 0.786 * diff,    # Deep retracement
        "100.0%": low,                   # The Trough (Support)
    }

    return levels