from models.greeks import compute_greeks
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Back, Style, init
init(autoreset=True)

def format_chain(spot, strikes, calls, puts, gex_by_strike, vanna_charm_data, lot_size,
                 t_expiry, rf_rate):
    """
    Build and print a table with ±5% strikes, rounded LTP to 0, Greeks to 4 decimals,
    yellow background for LTP < 10.
    """
    lower = spot * 0.95
    upper = spot * 1.05
    filtered_strikes = [s for s in strikes if lower <= s <= upper]
    if not filtered_strikes:
        filtered_strikes = strikes[:20]  # fallback
    
    rows = []
    for strike in filtered_strikes:
        # Call
        call_ltp = calls.loc[strike, "ltp"] if strike in calls.index else 0
        call_oi = calls.loc[strike, "oi"] if strike in calls.index else 0
        call_iv = calls.loc[strike, "iv"] if strike in calls.index else 0
        call_greeks = compute_greeks(spot, strike, t_expiry, rf_rate, call_iv, "call") if call_oi>0 else {}
        # Put
        put_ltp = puts.loc[strike, "ltp"] if strike in puts.index else 0
        put_oi = puts.loc[strike, "oi"] if strike in puts.index else 0
        put_iv = puts.loc[strike, "iv"] if strike in puts.index else 0
        put_greeks = compute_greeks(spot, strike, t_expiry, rf_rate, put_iv, "put") if put_oi>0 else {}
        
        row = {
            "Strike": strike,
            "Call LTP": int(round(call_ltp)),
            "Call OI": f"{call_oi//1000}k" if call_oi >= 1000 else str(call_oi),
            "Call IV%": f"{call_iv*100:.2f}",
            "Call Delta": f"{call_greeks.get('delta',0):.4f}",
            "Call Gamma": f"{call_greeks.get('gamma',0):.4f}",
            "Call GEX(Cr)": f"{gex_by_strike.get(strike,0)/1e7:.1f}",
            "Call Vanna": f"{call_greeks.get('vanna',0):.4f}",
            "Call Charm": f"{call_greeks.get('charm',0):.4f}",
            "Put LTP": int(round(put_ltp)),
            "Put OI": f"{put_oi//1000}k" if put_oi >= 1000 else str(put_oi),
            "Put IV%": f"{put_iv*100:.2f}",
            "Put Delta": f"{put_greeks.get('delta',0):.4f}",
            "Put Gamma": f"{put_greeks.get('gamma',0):.4f}",
            "Put GEX(Cr)": f"{-gex_by_strike.get(strike,0)/1e7:.1f}",  # put contribution negative in net
            "Put Vanna": f"{put_greeks.get('vanna',0):.4f}",
            "Put Charm": f"{put_greeks.get('charm',0):.4f}",
        }
        rows.append(row)
    
    # Convert to DataFrame for styling
    df = pd.DataFrame(rows)
    
    # Print with tabulate and color yellow for LTP < 10
    def color_ltp(val, col):
        if col in ("Call LTP", "Put LTP") and isinstance(val, int) and val < 10:
            return Back.YELLOW + Fore.BLACK + str(val) + Style.RESET_ALL
        return str(val)
    
    # Manual tabulate with colored cells
    headers = df.columns.tolist()
    table_data = []
    for _, row in df.iterrows():
        colored_row = []
        for col in headers:
            val = row[col]
            if col in ("Call LTP", "Put LTP") and isinstance(val, int) and val < 10:
                colored_row.append(Back.YELLOW + Fore.BLACK + str(val) + Style.RESET_ALL)
            else:
                colored_row.append(str(val))
        table_data.append(colored_row)
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("\nNote: Yellow background indicates LTP < 10 (cheap options).\n")
