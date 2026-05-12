# GEX Structural Analysis Terminal for NIFTY & BANKNIFTY

Replicates the SPX GEX terminal for Indian indices using Kite API.

## Setup

1. Install Python 3.9+
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your Kite credentials.
4. Run `python run_nifty.py`

## Features

- Fetch real-time option chain for NIFTY (weekly) and BANKNIFTY (monthly)
- Compute Gamma Exposure (GEX), Gamma Flip, Max +GEX/-GEX
- Gamma Implied Volatility (GIV), Skew metrics
- Vanna & Charm exposures
- Strategy bias based on regime (Green/Red)
- Option chain table with ±5% strikes, yellow background for LTP < 10

## Output

Terminal prints summary and a colored table. Also exports to Excel (optional).

## Notes

- Lot sizes: NIFTY=65, BANKNIFTY=30 (effective Jan 2026)
- Expiry: NIFTY weekly Tuesdays, BANKNIFTY last Tuesday of month
- Rate limits: 1 request/sec, batch quotes 500 instruments.