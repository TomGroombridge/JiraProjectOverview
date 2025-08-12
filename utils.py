from datetime import datetime, timedelta
from config import BANK_HOLIDAYS

def working_days_between(start_date, end_date, holidays=BANK_HOLIDAYS):
    """
    Returns a list of working days (Mon-Fri, excluding holidays) between two dates (inclusive).
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    delta = (end_date - start_date).days + 1
    all_days = [start_date + timedelta(days=i) for i in range(delta)]

    working_days = [
        d for d in all_days
        if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in holidays
    ]
    return working_days
