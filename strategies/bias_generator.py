def get_bias_text(regime):
    if "GREEN" in regime:
        return ("Fade extremes, sell rips / buy dips, short volatility",
                "Tighter stops, expect range-bound action")
    else:
        return ("Follow the trend, long volatility, use breakouts",
                "Wider stops, reduce leverage")
