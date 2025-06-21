import pandas as pd
from datetime import datetime, timedelta
import os

def cleanup():
    file = "schedules.xlsx"
    if not os.path.exists(file):
        return  # Nothing to clean up yet

    df = pd.read_excel(file, engine="openpyxl")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    one_month_ago = datetime.today() - timedelta(days=30)
    df = df[df["Date"] >= one_month_ago]
    df.to_excel(file, index=False, engine="openpyxl")