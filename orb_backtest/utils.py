
# Hardcoded lists for simplicity and reliability in a demo app.
# In a production app, these might be scraped from NSE website or fetched from a CSV.

NIFTY_50 = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY",
    "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITC",
    "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT",
    "LTIM", "M&M", "MARUTI", "NESTLEIND", "NTPC",
    "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN",
    "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS", "TATACONSUM",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]

# A small subset for other indices to demonstrate functionality without bloating the file too much
NIFTY_BANK = [
    "AUBANK", "AXISBANK", "BANDHANBNK", "BANKBARODA", "FEDERALBNK",
    "HDFCBANK", "ICICIBANK", "IDFCFIRSTB", "INDUSINDBK", "KOTAKBANK",
    "PNB", "SBIN"
]

def get_index_constituents(index_name):
    """Returns a list of symbols for the given index."""
    if index_name == "Nifty 50":
        return sorted(NIFTY_50)
    elif index_name == "Nifty Bank":
        return sorted(NIFTY_BANK)
    # Fallback or other indices can be added here
    # For the purpose of this demo, we'll map others to Nifty 50 or a combined list
    if index_name == "Nifty 100":
        # Just returning Nifty 50 for now to keep it simple, or we could add more
        return sorted(NIFTY_50) 
    
    return sorted(NIFTY_50)
