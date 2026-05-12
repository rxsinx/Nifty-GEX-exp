from .greeks import compute_greeks

def compute_giv(strikes, calls, puts, spot, t_expiry, rf_rate, lot_size):
    """
    Returns (call_giv, put_giv, total_giv) as decimals (e.g., 0.165)
    """
    total_gamma = 0.0
    total_iv_gamma = 0.0
    call_gamma_sum = 0.0
    put_gamma_sum = 0.0
    call_iv_sum = 0.0
    put_iv_sum = 0.0
    
    for strike in strikes:
        # Call
        call_oi = calls.loc[strike, "oi"] if strike in calls.index else 0
        call_iv = calls.loc[strike, "iv"] if strike in calls.index else 0.0
        call_gamma = 0.0
        if call_oi > 0 and call_iv > 0:
            greeks = compute_greeks(spot, strike, t_expiry, rf_rate, call_iv, "call")
            call_gamma = greeks["gamma"]
        call_weight = call_gamma * call_oi * lot_size
        total_gamma += call_weight
        total_iv_gamma += call_iv * call_weight
        call_gamma_sum += call_weight
        call_iv_sum += call_iv * call_weight
        
        # Put
        put_oi = puts.loc[strike, "oi"] if strike in puts.index else 0
        put_iv = puts.loc[strike, "iv"] if strike in puts.index else 0.0
        put_gamma = 0.0
        if put_oi > 0 and put_iv > 0:
            greeks = compute_greeks(spot, strike, t_expiry, rf_rate, put_iv, "put")
            put_gamma = greeks["gamma"]
        put_weight = put_gamma * put_oi * lot_size
        total_gamma += put_weight
        total_iv_gamma += put_iv * put_weight
        put_gamma_sum += put_weight
        put_iv_sum += put_iv * put_weight
    
    call_giv = call_iv_sum / call_gamma_sum if call_gamma_sum > 0 else 0.0
    put_giv = put_iv_sum / put_gamma_sum if put_gamma_sum > 0 else 0.0
    total_giv = total_iv_gamma / total_gamma if total_gamma > 0 else 0.0
    return call_giv, put_giv, total_giv
