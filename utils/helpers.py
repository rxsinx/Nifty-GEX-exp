import pandas as pd
from datetime import datetime

def round_ltp(ltp):
    return int(round(ltp))

def round_greeks(value, decimals=4):
    return round(value, decimals)

def format_oi(oi):
    if oi >= 1_000_000:
        return f"{oi/1_000_000:.1f}M"
    elif oi >= 1_000:
        return f"{oi//1_000}k"
    else:
        return str(oi)

def days_to_expiry(expiry_date_str):
    expiry = pd.to_datetime(expiry_date_str)
    now = datetime.now()
    delta = expiry - now
    return max(delta.days, 0)
