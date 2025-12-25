# Stock-Market-Analyzer
# 📈 FiboBot - AI-Driven Trading Analyzer

An advanced algorithmic trading tool that automates technical analysis using **Fibonacci Retracement levels**. Built with **Python** and **Streamlit**, it monitors Cryptocurrencies and Stock Markets in real-time to generate Buy/Sell signals based on price breakouts.

## Key Features
* **Multi-Market Support:** Analyzes both Crypto (Binance pairs) and US Stocks (NASDAQ/NYSE).
* **Smart Signal Generation:** Automatically detects breakouts above/below key Fibonacci levels (e.g., 61.8% "Golden Ratio").
* **Interactive Dashboard:** A full-featured web UI built with **Streamlit** for real-time monitoring.
* **Visual Analytics:** Dynamic, zoomable candlestick charts powered by **Plotly**.
* **Modular Architecture:** Clean separation between business logic (`core`) and frontend (`app`).

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **UI Framework:** Streamlit
* **Data Analysis:** Pandas, NumPy
* **APIs & Data Fetching:** yfinance, CCXT, TradingView-TA
* **Visualization:** Plotly Graph Objects
* **Machine Learning:** Scikit-learn (for trend prediction features)

## ⚙️ Installation & Usage
To run the dashboard locally on your machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Stock-Market-Analyzer.git](https://github.com/YOUR_USERNAME/Stock-Market-Analyzer.git)
    cd Stock-Market-Analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    *The dashboard will open automatically in your browser.*

## 📂 Project Structure
* `app.py` / `main.py` - The entry point for the Streamlit dashboard.
* `core/` - Contains the algorithmic logic (Signal generation, Fibonacci calculations).
* `requirements.txt` - List of required Python libraries.

## ⚠️ Disclaimer
This project is developed for educational and research purposes only. It does not constitute financial advice.
