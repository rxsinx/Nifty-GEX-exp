from config.settings import RISK_FREE_RATE
from strategies.regime_detector import get_regime
from strategies.bias_generator import get_bias_text

def format_number(num):
    if abs(num) >= 1e12:
        return f"{num/1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"{num/1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"{num/1e6:.2f}M"
    else:
        return f"{num:.0f}"

def print_summary(symbol, spot, gamma_flip, max_gex_strike, max_gex_val, min_gex_strike, min_gex_val,
                  total_gex_oi, total_gex_vol, call_giv, put_giv, total_giv, atm_iv,
                  rr_25d, skew_giv_ratio, total_vanna, total_charm, dte):
    regime = get_regime(total_gex_oi)
    bias_text, risk_text = get_bias_text(regime)
    
    print("\n" + "="*80)
    print(f" {symbol} OPTIONS GEX STRUCTURAL ANALYSIS - {dte} DTE")
    print("="*80)
    print(f" Spot: {spot:,.2f} | Risk-free: {RISK_FREE_RATE:.2%} | Gamma Flip: {gamma_flip}")
    print(f" Max +GEX: {max_gex_strike} ({format_number(max_gex_val)}) | Max -GEX: {min_gex_strike} ({format_number(min_gex_val)})")
    print("-"*80)
    print(f" GEX Metrics: Total GEX (OI): {format_number(total_gex_oi)} | Total GEX (Vol): {format_number(total_gex_vol)}")
    print(f" Net Position: {'POSITIVE (Dealers Long Gamma)' if total_gex_oi > 0 else 'NEGATIVE (Dealers Short Gamma)'}")
    print("-"*80)
    print(f" GIV Analysis: Call GIV: {call_giv:.2%} | Put GIV: {put_giv:.2%} | Total GIV: {total_giv:.2%} | ATM IV: {atm_iv:.2%}")
    print(f" Skew Metrics: 25Δ RR: {rr_25d*100:.2f}% | Skew/GIV Ratio: {skew_giv_ratio:.4f}")
    print("-"*80)
    print(f" Vanna/Charm: Total Vanna: {format_number(total_vanna)} | Total Charm: {format_number(total_charm)}")
    print("-"*80)
    print(f" >> REGIME: {regime} -> Strategy Bias: {bias_text}")
    print(f"    Risk Management: {risk_text}")
    print("="*80 + "\n")
