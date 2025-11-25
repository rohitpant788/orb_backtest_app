# NSE ORB Backtester

A Streamlit application to backtest the **Opening Range Breakout (ORB)** strategy on Indian NSE stocks using free intraday data.

## Features

- **Index Selection**: Choose from Nifty 50, Nifty Bank, or Nifty 100 universes.
- **Dynamic Data**: Fetches real-time/historical intraday data using `yfinance`.
- **Customizable Strategy**:
  - Adjustable Opening Range duration (5, 10, 15, 30, 60 minutes).
  - Long Only, Short Only, or Both Sides.
  - Optional Stop Loss (at opposite ORB level) and End-of-Day exit.
- **Visualizations**:
  - Interactive Candlestick charts with ORB High/Low overlays.
  - Trade entry and exit markers.
- **Metrics**: Comprehensive performance stats including Win Rate, Total P&L, and Max Drawdown.

## Installation

1. **Clone the repository** or download the source code.
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default browser (usually at `http://localhost:8501`).

## Data Limitations

- The app uses `yfinance` for free data.
- **Intraday data is typically limited to the last 60 days**.
- If you select a date range older than 60 days for intraday intervals (1m, 5m, 15m), data may not be available.

## Usage
https://orbbacktestapp-mkcsqzktqby3eua6hgycic.streamlit.app/

## Disclaimer

This tool is for educational and backtesting purposes only. It is not a recommendation to trade. Trading in stock markets involves risk.
