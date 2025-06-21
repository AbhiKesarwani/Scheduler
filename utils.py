import os
from openpyxl import load_workbook
from datetime import datetime

def cleanup():
    file = "schedules.xlsx"
    if not os.path.exists(file):
        return

    wb = load_workbook(file)
    today = datetime.today().date()

    for sheet in wb.sheetnames:
        try:
            sheet_date = datetime.strptime(sheet, "%Y-%m-%d").date()
            if sheet_date < today:
                wb.remove(wb[sheet])
        except ValueError:
            continue  # skip sheets without valid date names

    wb.save(file)