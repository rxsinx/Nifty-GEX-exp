import greeks_package as gp
import pandas as pd
import numpy as np

def compute_greeks(spot, strike, t_expiry, rf_rate, iv, option_type):
    """
    Returns dict with all Greeks (delta, gamma, vega, theta, vanna, charm)
    using the greeks-package.
    """
    if iv <= 0:
        return {
            "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0,
            "vanna": 0.0, "charm": 0.0
        }
    try:
        delta = gp.delta(spot, strike, t_expiry, rf_rate, iv, option_type)
        gamma = gp.gamma(spot, strike, t_expiry, rf_rate, iv, option_type)
        vega = gp.vega(spot, strike, t_expiry, rf_rate, iv, option_type)
        theta = gp.theta(spot, strike, t_expiry, rf_rate, iv, option_type)
        vanna = gp.vanna(spot, strike, t_expiry, rf_rate, iv, option_type)
        charm = gp.charm(spot, strike, t_expiry, rf_rate, iv, option_type)
    except Exception as e:
        # fallback to zeros if errors (e.g., extreme strikes)
        return {
            "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0,
            "vanna": 0.0, "charm": 0.0
        }
    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "vanna": vanna,
        "charm": charm
    }
