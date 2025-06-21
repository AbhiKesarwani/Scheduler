import pandas as pd
import os

SCHEDULE_FILE = "schedules.xlsx"
HEADERS = ["User", "Date", "Start", "End", "Class"]

def initialize_schedule_file():
    if not os.path.exists(SCHEDULE_FILE):
        df = pd.DataFrame(columns=HEADERS)
        df.to_excel(SCHEDULE_FILE, index=False, engine="openpyxl")

def read_schedule():
    initialize_schedule_file()
    return pd.read_excel(SCHEDULE_FILE, engine="openpyxl")

def write_schedule(new_entry):
    df = read_schedule()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(SCHEDULE_FILE, index=False, engine="openpyxl")