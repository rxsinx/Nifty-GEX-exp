#!/usr/bin/env python3
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
from login_helper import login_and_inject

logger = setup_logger()

def main():
    # 1. Login and inject Kite instance
    login_and_inject()

    symbol = "NIFTY"
    try:
        spot = get_spot(symbol)
        expiry_date = get_expiry_date(symbol, expiry_type="weekly")
        logger.info(f"Expiry: {expiry_date}")
        strikes, calls, puts = get_option_chain(symbol, expiry_date.strftime("%Y-%m-%d"))
        t_expiry = (expiry_date - datetime.now()).days / 365.0
        if t_expiry <= 0:
            logger.error("Expiry passed or today is expiry day.")
            sys.exit(1)

        lot_size = LOT_SIZES[symbol]
        total_gex_oi, gex_by_strike = total_gex_and_by_strike(strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size)
        gamma_flip = gamma_flip_strike(strikes, gex_by_strike)
        max_gex_strike, max_gex_val, min_gex_strike, min_gex_val = max_min_gex_strikes(gex_by_strike)

        call_giv, put_giv, total_giv = compute_giv(strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size)
        atm_strike = min(strikes, key=lambda x: abs(x - spot))
        atm_iv = calls.loc[atm_strike, "iv"] if atm_strike in calls.index else total_giv

        rr_25d = -0.136  # placeholder
        skew_giv_ratio = (put_giv - call_giv) / total_giv if total_giv != 0 else 0.0

        total_vanna, total_charm, _ = total_vanna_charm(strikes, calls, puts, spot, t_expiry, RISK_FREE_RATE, lot_size)

        dte = (expiry_date - datetime.now()).days

        print_summary(symbol, spot, gamma_flip, max_gex_strike, max_gex_val, min_gex_strike, min_gex_val,
                      total_gex_oi, total_gex_oi, call_giv, put_giv, total_giv, atm_iv,
                      rr_25d, skew_giv_ratio, total_vanna, total_charm, dte)

        format_chain(spot, strikes, calls, puts, gex_by_strike, {}, lot_size, t_expiry, RISK_FREE_RATE)

    except Exception as e:
        logger.exception("Error in NIFTY analysis")
        sys.exit(1)

if __name__ == "__main__":
    main()
