#!/usr/bin/env python3
"""
GEX Terminal for BANKNIFTY (monthly expiry only, lot size = 30)
"""

import sys
from datetime import datetime
from config.settings import LOT_SIZES, RISK_FREE_RATE
from config.expiry_rules import get_expiry_date
from data.data_fetcher import get_spot, get_option_chain
from models.gex import total_gex_and_by_strike, gamma_flip_strike, max_min_gex_strikes
from models.giv import compute_giv
from models.vanna_charm import total_vanna_charm
from output.terminal_formatter import print_summary
from output.option_chain_formatter import format_chain
from utils.logger import setup_logger

logger = setup_logger()

def main():
    symbol = "BANKNIFTY"
    try:
        # 1. Get spot price
        spot = get_spot(symbol)
        logger.info(f"{symbol} Spot: {spot:.2f}")

        # 2. Get next monthly expiry (last Tuesday)
        expiry_date = get_expiry_date(symbol, expiry_type="monthly")
        logger.info(f"Monthly expiry: {expiry_date.strftime('%Y-%m-%d')}")

        # 3. Fetch option chain for that expiry
        strikes, calls, puts = get_option_chain(symbol, expiry_date.strftime("%Y-%m-%d"))

        # 4. Time to expiry (in years)
        t_expiry = (expiry_date - datetime.now()).days / 365.0
        if t_expiry <= 0:
            logger.error("Expiry passed or today is expiry day. No analysis possible.")
            sys.exit(1)

        # 5. Lot size (revised for BANKNIFTY = 30)
        lot_size = LOT_SIZES[symbol]

        # 6. GEX calculations
        total_gex_oi, gex_by_strike = total_gex_and_by_strike(
            strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size
        )
        gamma_flip = gamma_flip_strike(strikes, gex_by_strike)
        max_gex_strike, max_gex_val, min_gex_strike, min_gex_val = max_min_gex_strikes(gex_by_strike)

        # 7. GIV (Gamma Implied Volatility)
        call_giv, put_giv, total_giv = compute_giv(
            strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size
        )

        # 8. ATM implied volatility (closest strike to spot)
        atm_strike = min(strikes, key=lambda x: abs(x - spot))
        atm_iv = calls.loc[atm_strike, "iv"] if atm_strike in calls.index else total_giv

        # 9. Skew metrics (simplified placeholder – you can implement full smile later)
        rr_25d = -0.136   # example; real calculation from chain recommended
        skew_giv_ratio = (put_giv - call_giv) / total_giv if total_giv != 0 else 0.0

        # 10. Vanna & Charm
        total_vanna, total_charm, vanna_centroid = total_vanna_charm(
            strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size
        )

        # 11. Days to expiry (for terminal header)
        dte = (expiry_date - datetime.now()).days

        # 12. Print terminal summary
        print_summary(
            symbol, spot, gamma_flip,
            max_gex_strike, max_gex_val, min_gex_strike, min_gex_val,
            total_gex_oi, total_gex_oi,   # Volume‑based GEX placeholder (use same if no volume data)
            call_giv, put_giv, total_giv, atm_iv,
            rr_25d, skew_giv_ratio,
            total_vanna, total_charm,
            dte
        )

        # 13. Print option chain (±5% strikes, coloured LTP)
        format_chain(spot, strikes, calls, puts, gex_by_strike, {}, lot_size, t_expiry, RISK_FREE_RATE)

    except Exception as e:
        logger.exception(f"Error in {symbol} analysis")
        sys.exit(1)

if __name__ == "__main__":
    main()
