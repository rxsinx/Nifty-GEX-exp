import numpy as np
from .greeks import compute_greeks

def compute_gex_per_strike(spot, strike, t_expiry, rf_rate, iv, oi, lot_size, option_type):
    """GEX in INR (not crores)."""
    greeks = compute_greeks(spot, strike, t_expiry, rf_rate, iv, option_type)
    gamma = greeks["gamma"]
    if gamma <= 0:
        return 0.0
    gex = gamma * oi * lot_size * (spot ** 2) * 0.01
    return gex

def total_gex_and_by_strike(strikes, calls, puts, spot, t_expiry, rf_rate, lot_size):
    gex_by_strike = {}
    total_gex = 0.0
    for strike in strikes:
        # Call side
        call_oi = calls.loc[strike, "oi"] if strike in calls.index else 0
        call_iv = calls.loc[strike, "iv"] if strike in calls.index else 0.0
        call_gex = compute_gex_per_strike(spot, strike, t_expiry, rf_rate, call_iv, call_oi, lot_size, "call")
        # Put side
        put_oi = puts.loc[strike, "oi"] if strike in puts.index else 0
        put_iv = puts.loc[strike, "iv"] if strike in puts.index else 0.0
        put_gex = compute_gex_per_strike(spot, strike, t_expiry, rf_rate, put_iv, put_oi, lot_size, "put")
        net_gex = call_gex - put_gex
        gex_by_strike[strike] = net_gex
        total_gex += net_gex
    return total_gex, gex_by_strike

def gamma_flip_strike(strikes, gex_by_strike):
    """Return strike where cumulative GEX crosses zero from negative to positive."""
    sorted_strikes = sorted(strikes)
    cumsum = 0.0
    for strike in sorted_strikes:
        cumsum += gex_by_strike.get(strike, 0.0)
        if cumsum > 0:
            return strike
    return sorted_strikes[0] if sorted_strikes else None

def max_min_gex_strikes(gex_by_strike):
    """Return (max_gex_strike, max_gex_value), (min_gex_strike, min_gex_value)"""
    strikes = list(gex_by_strike.keys())
    if not strikes:
        return None, None, None, None
    max_strike = max(gex_by_strike, key=gex_by_strike.get)
    min_strike = min(gex_by_strike, key=gex_by_strike.get)
    return max_strike, gex_by_strike[max_strike], min_strike, gex_by_strike[min_strike]
