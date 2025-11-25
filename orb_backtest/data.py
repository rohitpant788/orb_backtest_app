import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import timedelta

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_stock_data(symbol, start_date, end_date, interval="5m"):
    """
    Fetches intraday data for a given symbol from yfinance.
    
    Args:
        symbol (str): NSE symbol (e.g., "RELIANCE").
        start_date (date): Start date.
        end_date (date): End date.
        interval (str): Intraday interval (e.g., "5m", "15m").
        
    Returns:
        pd.DataFrame: OHLC data.
    """
    # Append .NS if not present
    if not symbol.endswith(".NS"):
        ticker_symbol = f"{symbol}.NS"
    else:
        ticker_symbol = symbol
        
    # yfinance download
    # Note: yfinance end_date is exclusive, so we might need to add a day if we want to include the end_date fully
    # However, for intraday, it usually works fine with dates.
    
    try:
        df = yf.download(
            tickers=ticker_symbol,
            start=start_date,
            end=end_date + timedelta(days=1), # Add 1 day to include the end date
            interval=interval,
            progress=False,
            multi_level_index=False # Ensure flat columns
        )
        
        if df.empty:
            return pd.DataFrame()
            
        # Ensure timezone is localized/converted properly if needed, 
        # but usually yfinance returns tz-aware index for intraday.
        # We'll drop rows with NaN values just in case
        df.dropna(inplace=True)
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()
