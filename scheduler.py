import streamlit as st
from datetime import date, time
from db import write_schedule, read_schedule
import pandas as pd

def schedule_form(user):
    st.subheader("Add Schedule")
    sched_date = st.date_input("Date", value=date.today())
    start_time = st.time_input("Start Time", value=time(9, 0))
    end_time = st.time_input("End Time", value=time(10, 0))
    class_info = st.text_input("Class Number / Notes")

    if st.button("Save"):
        entry = {
            "User": user,
            "Date": str(sched_date),
            "Start": str(start_time),
            "End": str(end_time),
            "Class": class_info
        }
        write_schedule(entry)
        st.success("Schedule saved!")

def view_schedule(user):
    st.subheader("My Schedule")
    selected_date = st.date_input("Select Date to View", value=date.today())
    df = read_schedule()
    user_df = df[df["User"] == user]
    day_df = user_df[user_df["Date"] == str(selected_date)]

    if day_df.empty:
        st.info("No entries for this date.")
    else:
        st.dataframe(day_df)