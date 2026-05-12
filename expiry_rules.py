from datetime import datetime, timedelta
import pandas as pd
from .settings import NSE_HOLIDAYS

def get_next_weekday(start_date, target_weekday):
    """
    Get next occurrence of target_weekday (0=Monday, 1=Tuesday, ... 6=Sunday)
    """
    days_ahead = (target_weekday - start_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return start_date + timedelta(days=days_ahead)

def get_last_weekday(year, month, target_weekday):
    """
    Get last occurrence of target_weekday in given month.
    """
    last_day = datetime(year, month, 1) + timedelta(days=32)
    last_day = last_day.replace(day=1) - timedelta(days=1)
    while last_day.weekday() != target_weekday:
        last_day -= timedelta(days=1)
    return last_day

def adjust_for_holiday(date):
    """If date is holiday, move to previous trading day."""
    while date.strftime("%Y-%m-%d") in NSE_HOLIDAYS:
        date -= timedelta(days=1)
    return date

def get_next_weekly_expiry(reference_date=None):
    """
    Next Tuesday expiry (NIFTY weekly).
    Holidays: preponed to previous day.
    """
    if reference_date is None:
        reference_date = datetime.now()
    tuesday = get_next_weekday(reference_date, 1)  # 1 = Tuesday
    return adjust_for_holiday(tuesday)

def get_next_monthly_expiry(reference_date=None):
    """
    Next last Tuesday expiry (NIFTY & BANKNIFTY monthly).
    """
    if reference_date is None:
        reference_date = datetime.now()
    # Start from the first day of next month if today is after last Tuesday of current month
    # Simpler: find last Tuesday of current month; if before today, go to next month.
    year, month = reference_date.year, reference_date.month
    last_tue = get_last_weekday(year, month, 1)
    if last_tue < reference_date:
        # Move to next month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        last_tue = get_last_weekday(year, month, 1)
    return adjust_for_holiday(last_tue)

def get_expiry_date(symbol, expiry_type="weekly", ref_date=None):
    """
    expiry_type: 'weekly' (only for NIFTY) or 'monthly'
    """
    if symbol == "NIFTY" and expiry_type == "weekly":
        return get_next_weekly_expiry(ref_date)
    else:
        return get_next_monthly_expiry(ref_date)
