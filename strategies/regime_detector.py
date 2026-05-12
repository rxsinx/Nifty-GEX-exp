def get_regime(total_gex):
    return "GREEN (Mean Reversion)" if total_gex > 0 else "RED (Trend/Momentum)"
