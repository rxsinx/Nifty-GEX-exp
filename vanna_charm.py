from .greeks import compute_greeks

def total_vanna_charm(strikes, calls, puts, spot, t_expiry, rf_rate, lot_size):
    total_vanna = 0.0
    total_charm = 0.0
    vanna_by_strike = {}
    
    for strike in strikes:
        # Call vanna/charm
        call_oi = calls.loc[strike, "oi"] if strike in calls.index else 0
        call_iv = calls.loc[strike, "iv"] if strike in calls.index else 0.0
        if call_oi > 0 and call_iv > 0:
            greeks = compute_greeks(spot, strike, t_expiry, rf_rate, call_iv, "call")
            call_vanna = greeks["vanna"] * call_oi * lot_size * spot
            call_charm = greeks["charm"] * call_oi * lot_size * spot
            total_vanna += call_vanna
            total_charm += call_charm
        # Put vanna/charm
        put_oi = puts.loc[strike, "oi"] if strike in puts.index else 0
        put_iv = puts.loc[strike, "iv"] if strike in puts.index else 0.0
        if put_oi > 0 and put_iv > 0:
            greeks = compute_greeks(spot, strike, t_expiry, rf_rate, put_iv, "put")
            put_vanna = greeks["vanna"] * put_oi * lot_size * spot
            put_charm = greeks["charm"] * put_oi * lot_size * spot
            total_vanna += put_vanna
            total_charm += put_charm
        vanna_by_strike[strike] = (call_vanna if call_oi else 0) + (put_vanna if put_oi else 0)
    
    # Vanna centroid: strike where cumulative vanna crosses 50% of total
    # Simple: strike with max absolute vanna (or weighted average)
    if vanna_by_strike:
        centroid = sum(k * abs(v) for k, v in vanna_by_strike.items()) / sum(abs(v) for v in vanna_by_strike.values())
    else:
        centroid = spot
    return total_vanna, total_charm, centroid
