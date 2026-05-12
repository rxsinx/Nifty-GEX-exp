import time
import pandas as pd
from .kite_client import KiteClient
from config.settings import QUOTES_BATCH_SIZE, REQUEST_SLEEP, KITE_SYMBOLS
from config.expiry_rules import get_expiry_date
import logging

logger = logging.getLogger(__name__)

client = KiteClient()

def get_spot(symbol):
    """Return current spot price for NIFTY or BANKNIFTY."""
    ltp_data = client.ltp(KITE_SYMBOLS[symbol])
    return ltp_data[KITE_SYMBOLS[symbol]]["last_price"]

def get_option_chain(symbol, expiry_date):
    """
    Returns:
        strikes: list of int
        calls_df: DataFrame with index=strike, columns = oi, ltp, iv
        puts_df: same
    """
    instruments = client.get_instruments("NFO")
    # Filter for symbol, expiry, CE/PE
    options = instruments[
        (instruments["name"] == symbol) &
        (instruments["expiry"] == expiry_date) &
        (instruments["instrument_type"].isin(["CE", "PE"]))
    ].copy()
    
    if options.empty:
        raise ValueError(f"No options found for {symbol} expiry {expiry_date}")
    
    # Batch fetch quotes
    tokens = options["instrument_token"].tolist()
    quotes = {}
    for i in range(0, len(tokens), QUOTES_BATCH_SIZE):
        batch = tokens[i:i+QUOTES_BATCH_SIZE]
        batch_quotes = client.get_quotes(batch)
        quotes.update(batch_quotes)
        time.sleep(REQUEST_SLEEP)
    
    # Extract OI, LTP, IV
    options["oi"] = options["instrument_token"].apply(lambda t: quotes.get(t, {}).get("oi", 0))
    options["ltp"] = options["instrument_token"].apply(lambda t: quotes.get(t, {}).get("last_price", 0))
    options["iv"] = options["instrument_token"].apply(lambda t: quotes.get(t, {}).get("implied_volatility", 0)) / 100.0  # as decimal
    
    # Separate calls and puts
    calls = options[options["instrument_type"] == "CE"].set_index("strike")
    puts = options[options["instrument_type"] == "PE"].set_index("strike")
    
    strikes = sorted(set(calls.index) | set(puts.index))
    return strikes, calls, puts
