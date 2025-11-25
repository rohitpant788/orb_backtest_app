import pandas as pd
import numpy as np

def calculate_orb_levels(df, orb_minutes):
    """
    Calculates ORB High and Low for each day.
    
    Args:
        df (pd.DataFrame): Intraday OHLC data with Datetime index.
        orb_minutes (int): Opening range duration in minutes.
        
    Returns:
        pd.DataFrame: DataFrame with 'ORB_High' and 'ORB_Low' columns mapped to each timestamp.
    """
    df = df.copy()
    df['Date'] = df.index.date
    
    orb_levels = {}
    
    # Group by date to process each day
    for date, day_data in df.groupby('Date'):
        if day_data.empty:
            continue
            
        # Define the ORB end time
        start_time = day_data.index[0]
        orb_end_time = start_time + pd.Timedelta(minutes=orb_minutes)
        
        # Filter data for the opening range
        orb_data = day_data[day_data.index < orb_end_time]
        
        if orb_data.empty:
            continue
            
        orb_high = orb_data['High'].max()
        orb_low = orb_data['Low'].min()
        
        orb_levels[date] = (orb_high, orb_low, orb_end_time)
        
    return orb_levels

def run_backtest(df, orb_minutes, direction, use_sl, exit_eod):
    """
    Runs the ORB backtest.
    
    Args:
        df (pd.DataFrame): Intraday OHLC data.
        orb_minutes (int): ORB duration.
        direction (str): "Long Only", "Short Only", "Both".
        use_sl (bool): Whether to use opposite ORB level as SL.
        exit_eod (bool): Whether to exit at EOD.
        
    Returns:
        list: List of trades (dicts).
    """
    orb_levels = calculate_orb_levels(df, orb_minutes)
    trades = []
    
    df['Date'] = df.index.date
    
    for date, day_data in df.groupby('Date'):
        if date not in orb_levels:
            continue
            
        orb_high, orb_low, orb_end_time = orb_levels[date]
        
        # Filter data AFTER the opening range
        trading_data = day_data[day_data.index >= orb_end_time]
        
        if trading_data.empty:
            continue
            
        position = None # 'Long' or 'Short'
        entry_price = 0.0
        entry_time = None
        stop_loss = 0.0
        
        for i in range(len(trading_data)):
            candle = trading_data.iloc[i]
            current_time = trading_data.index[i]
            
            # Check for Entry
            if position is None:
                # Long Entry
                if (direction in ["Long Only", "Both Sides"]) and (candle['Close'] > orb_high):
                    # Enter at next candle Open (simulated by current candle Close for simplicity in vectorization, 
                    # but strictly per requirements: "open of the next candle". 
                    # In a loop, we can peek next open, or assume fill at Close of breakout candle 
                    # OR fill at next Open. Let's try to fill at next Open if available.
                    
                    if i + 1 < len(trading_data):
                        next_candle = trading_data.iloc[i+1]
                        entry_price = next_candle['Open']
                        entry_time = trading_data.index[i+1]
                        position = 'Long'
                        stop_loss = orb_low if use_sl else 0.0
                        continue
                
                # Short Entry
                if (direction in ["Short Only", "Both Sides"]) and (candle['Close'] < orb_low):
                    if i + 1 < len(trading_data):
                        next_candle = trading_data.iloc[i+1]
                        entry_price = next_candle['Open']
                        entry_time = trading_data.index[i+1]
                        position = 'Short'
                        stop_loss = orb_high if use_sl else float('inf')
                        continue
                        
            # Check for Exit if in position
            else:
                # Check SL hit (Low hits SL for Long, High hits SL for Short)
                # We assume SL is hit during the candle
                
                exit_price = 0.0
                exit_reason = ""
                
                if position == 'Long':
                    if use_sl and (candle['Low'] <= stop_loss):
                        exit_price = stop_loss
                        exit_reason = "SL Hit"
                    elif i == len(trading_data) - 1 and exit_eod:
                        exit_price = candle['Close']
                        exit_reason = "EOD Exit"
                        
                elif position == 'Short':
                    if use_sl and (candle['High'] >= stop_loss):
                        exit_price = stop_loss
                        exit_reason = "SL Hit"
                    elif i == len(trading_data) - 1 and exit_eod:
                        exit_price = candle['Close']
                        exit_reason = "EOD Exit"
                
                if exit_price > 0:
                    pnl = exit_price - entry_price if position == 'Long' else entry_price - exit_price
                    pnl_pct = (pnl / entry_price) * 100
                    
                    trades.append({
                        'Date': date,
                        'Direction': position,
                        'Entry Time': entry_time,
                        'Entry Price': entry_price,
                        'Exit Time': current_time,
                        'Exit Price': exit_price,
                        'P&L': pnl,
                        'P&L (%)': pnl_pct,
                        'Exit Reason': exit_reason,
                        'ORB High': orb_high,
                        'ORB Low': orb_low
                    })
                    position = None # Reset position
                    break # One trade per day per requirements "only one active trade per day" (implied simple logic)
                    
    return pd.DataFrame(trades)
