import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

from orb_backtest.utils import get_index_constituents
from orb_backtest.data import get_stock_data
from orb_backtest.strategy import run_backtest

st.set_page_config(page_title="NSE ORB Backtester", layout="wide")

st.title("🇮🇳 NSE Intraday ORB Backtester")

# --- Sidebar ---
st.sidebar.header("Configuration")

# 1. Index Universe
index_name = st.sidebar.selectbox(
    "Index Universe",
    ["Nifty 50", "Nifty Bank", "Nifty 100"]
)

# 2. Stock Selection
symbols = get_index_constituents(index_name)
selected_symbol = st.sidebar.selectbox("Stock", symbols)

# 3. Parameters
st.sidebar.subheader("Strategy Parameters")
orb_minutes = st.sidebar.selectbox("Opening Range (minutes)", [5, 10, 15, 30, 60], index=2) # Default 15
interval = st.sidebar.selectbox("Candle Interval", ["1m", "5m", "15m", "30m"], index=1) # Default 5m

# Date Range
# yfinance limitation note
st.sidebar.info("Note: Free data is limited to ~60 days for intraday intervals.")
default_start = date.today() - timedelta(days=59)
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", date.today())

# Strategy Direction
direction = st.sidebar.radio(
    "Direction",
    ["Long Only", "Short Only", "Both Sides"],
    index=2
)

# Risk Settings
use_sl = st.sidebar.checkbox("Use Stop Loss (Opposite ORB)", value=True)
exit_eod = st.sidebar.checkbox("Exit at EOD", value=True)

# Run Button
if st.sidebar.button("Run Backtest", type="primary"):
    
    with st.spinner(f"Fetching data for {selected_symbol}..."):
        df = get_stock_data(selected_symbol, start_date, end_date, interval)
        
    if df.empty:
        st.error("No data found! Please check the symbol or date range (max 60 days for intraday).")
    else:
        # Run Backtest
        trades = run_backtest(df, orb_minutes, direction, use_sl, exit_eod)
        
        # --- Results ---
        if trades.empty:
            st.warning("No trades generated with current parameters.")
        else:
            # 1. Metrics
            st.subheader("Performance Metrics")
            
            total_trades = len(trades)
            win_trades = trades[trades['P&L'] > 0]
            loss_trades = trades[trades['P&L'] <= 0]
            win_rate = (len(win_trades) / total_trades) * 100
            
            total_pnl = trades['P&L'].sum()
            avg_pnl = trades['P&L'].mean()
            best_trade = trades['P&L'].max()
            worst_trade = trades['P&L'].min()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Trades", total_trades)
            col2.metric("Win Rate", f"{win_rate:.1f}%")
            col3.metric("Total P&L", f"{total_pnl:.2f}")
            col4.metric("Avg Trade P&L", f"{avg_pnl:.2f}")
            
            col5, col6 = st.columns(2)
            col5.metric("Best Trade", f"{best_trade:.2f}")
            col6.metric("Worst Trade", f"{worst_trade:.2f}")
            
            # 2. Trade List
            st.subheader("Trade Log")
            st.dataframe(trades.style.format({
                'Entry Price': '{:.2f}',
                'Exit Price': '{:.2f}',
                'P&L': '{:.2f}',
                'P&L (%)': '{:.2f}%',
                'ORB High': '{:.2f}',
                'ORB Low': '{:.2f}'
            }), use_container_width=True)
            
            # 3. Charts
            st.subheader("Trade Visualization")
            
            # Date selector for chart
            trade_dates = sorted(trades['Date'].unique())
            selected_chart_date = st.selectbox("Select Date to View", trade_dates)
            
            # Filter data for that day
            day_df = df[df.index.date == selected_chart_date]
            day_trades = trades[trades['Date'] == selected_chart_date]
            
            if not day_df.empty:
                fig = go.Figure()
                
                # Candlestick
                fig.add_trace(go.Candlestick(
                    x=day_df.index,
                    open=day_df['Open'],
                    high=day_df['High'],
                    low=day_df['Low'],
                    close=day_df['Close'],
                    name="Price"
                ))
                
                # ORB Lines
                if not day_trades.empty:
                    orb_high = day_trades.iloc[0]['ORB High']
                    orb_low = day_trades.iloc[0]['ORB Low']
                    
                    fig.add_hline(y=orb_high, line_dash="dash", line_color="green", annotation_text="ORB High")
                    fig.add_hline(y=orb_low, line_dash="dash", line_color="red", annotation_text="ORB Low")
                    
                    # Entry/Exit Markers
                    for _, trade in day_trades.iterrows():
                        # Entry
                        fig.add_trace(go.Scatter(
                            x=[trade['Entry Time']], 
                            y=[trade['Entry Price']],
                            mode='markers',
                            marker=dict(symbol='triangle-up' if trade['Direction'] == 'Long' else 'triangle-down', size=12, color='blue'),
                            name=f"{trade['Direction']} Entry"
                        ))
                        
                        # Exit
                        fig.add_trace(go.Scatter(
                            x=[trade['Exit Time']], 
                            y=[trade['Exit Price']],
                            mode='markers',
                            marker=dict(symbol='x', size=10, color='black'),
                            name="Exit"
                        ))
                
                fig.update_layout(
                    title=f"Intraday Chart - {selected_symbol} ({selected_chart_date})",
                    xaxis_title="Time",
                    yaxis_title="Price",
                    height=600,
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
