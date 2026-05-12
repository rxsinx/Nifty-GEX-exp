import os
from dotenv import load_dotenv

load_dotenv()

# Financial parameters (can still come from .env or default)
RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", 0.0703))

# Lot sizes (revised effective Jan 2026)
LOT_SIZES = {
    "NIFTY": 65,
    "BANKNIFTY": 30
}

# Kite instrument symbols
KITE_SYMBOLS = {
    "NIFTY": "NSE:NIFTY 50",
    "BANKNIFTY": "NSE:NIFTY BANK"
}

# API limits
QUOTES_BATCH_SIZE = 500
REQUEST_SLEEP = 1.0

# NSE holidays 2026
NSE_HOLIDAYS = [
    "2026-01-26", "2026-03-14", "2026-04-02", "2026-05-01",
    "2026-08-15", "2026-10-02", "2026-11-09", "2026-12-25",
]

WEEKLY_EXPIRY_DAY = "Tuesday"
MONTHLY_EXPIRY_DAY = "Tuesday"
