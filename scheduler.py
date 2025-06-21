import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, time
from db import write_schedule, read_schedule_sheet, remove_schedule_entry

def apply_background():
    st.markdown("""
        <style>
        body {
            background-color: #f2f6ff;
            background-image: url('https://www.transparenttextures.com/patterns/white-diamond.png');
        }
        </style>
    """, unsafe_allow_html=True)

apply_background()

def schedule_form(user):
    st.subheader("📝 Add Schedule")

    sched_date = st.date_input("Select Date", value=date.today(), min_value=date.today())
    start_time = st.time_input("Start Time", value=time(9, 0))
    end_time = st.time_input("End Time", value=time(10, 0))

    col1, col2 = st.columns(2)
    with col1:
        class_number = st.text_input("Class Number")
    with col2:
        description = st.text_input("Description")

    if st.button("Save Schedule"):
        sheet_name = str(sched_date)
        conflict = False

        # Check for conflicts if file and sheet exist
        if os.path.exists("schedules.xlsx"):
            try:
                df = pd.read_excel("schedules.xlsx", sheet_name=sheet_name, engine="openpyxl")
                df["Start"] = pd.to_datetime(df["Start"], errors='coerce').dt.time
                df["End"] = pd.to_datetime(df["End"], errors='coerce').dt.time

                for _, row in df.iterrows():
                    if row["User"] == user and class_number == str(row["Class"]):
                        existing_start = row["Start"]
                        existing_end = row["End"]
                        if start_time < existing_end and end_time > existing_start:
                            conflict = True
                            break
            except:
                pass

        if conflict:
            st.error(f"⚠️ Class conflict detected! You already have '{class_number}' at that time.")
            return

        entry = {
            "User": user,
            "Date": str(sched_date),
            "Start": str(start_time),
            "End": str(end_time),
            "Class": class_number,
            "Description": description
        }
        write_schedule(entry)

        # Notification Summary
        st.success("✅ Schedule added successfully!")
        with st.expander("View Saved Entry"):
            st.markdown(f"""
            **👤 User:** `{user}`  
            **📅 Date:** `{sched_date}`  
            **⏰ Time:** `{start_time} - {end_time}`  
            **🏷 Class:** `{class_number}`  
            **📝 Description:** `{description}`
            """)

def view_schedule(user):
    st.subheader("📅 View Schedule")
    today = date.today()
    selected_date = st.date_input("Select Date", min_value=today)
    sheet = str(selected_date)

    with st.spinner("Loading schedule..."):
        try:
            df = pd.read_excel("schedules.xlsx", sheet_name=sheet, engine="openpyxl")
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

            # Optional: sort by time
            if "Start" in df.columns:
                df = df.sort_values(by="Start")

            st.success(f"Showing schedule for {sheet}")
            st.dataframe(df, use_container_width=True)
        except:
            st.info("No entries found for this date.")

import streamlit as st
import pandas as pd
from datetime import date
from db import remove_schedule_entry

def delete_schedule(user):
    st.subheader("❌ Delete a Schedule Entry")
    sched_date = st.date_input("Select Date to Review", min_value=date.today())
    sheet_name = str(sched_date)

    try:
        df = pd.read_excel("schedules.xlsx", sheet_name=sheet_name, engine="openpyxl")
        user_entries = df[df["User"] == user].reset_index(drop=True)

        if user_entries.empty:
            st.info("No entries found for this date.")
            return

        st.markdown("### Your Schedule Entries:")
        for i, row in user_entries.iterrows():
            with st.expander(f"🕒 {row['Start']} - {row['End']} | {row['Class']}"):
                st.write(f"📚 **Description**: {row['Description']}")
                delete_trigger = st.button("🗑 Delete This Entry", key=f"del_button_{i}")

                if delete_trigger:
                    st.session_state["pending_delete"] = {
                        "class": row["Class"],
                        "start": row["Start"],
                        "index": i,
                        "date": sheet_name
                    }

        # If user pressed delete, now prompt for password
        if "pending_delete" in st.session_state:
            info = st.session_state["pending_delete"]
            st.warning(f"Please confirm deletion of **{info['class']}** on {info['date']}")
            password = st.text_input("Re-enter your password to confirm:", type="password", key="pw_check")

        if st.button("Confirm Deletion"):
            users_df = pd.read_excel("users.xlsx")
            match = users_df[(users_df["Username"] == user) & (users_df["Password"] == password)]
            if match.empty:
                st.error("❌ Incorrect password.")
            else:
                success = remove_schedule_entry(info["date"], user, info["class"], info["start"])

                # 🔽 INSERT YOUR SUCCESS/FAILURE MESSAGE RIGHT HERE
                if success:
                    st.success("✅ Entry deleted successfully.")
                    st.session_state.pop("pending_delete")
                    st.rerun()
                else:
                    st.error("❌ Could not delete the entry. Please try again.")

    except Exception as e:
        st.info("No schedule found for this date.")

def export_schedule_csv():
    st.subheader("📤 Export Schedules (Admin Only)")

    all_data = []
    try:
        xl = pd.ExcelFile("schedules.xlsx", engine="openpyxl")
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            df["Sheet"] = sheet
            all_data.append(df)

        combined = pd.concat(all_data, ignore_index=True)
        st.download_button("Download All Schedules as CSV", data=combined.to_csv(index=False),
                           file_name="all_schedules.csv", mime="text/csv")
    except Exception as e:
        st.warning("Could not export schedules.")

st.markdown("""
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #e6f0ff;
            color: #333;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            border-top: 1px solid #ccc;
            z-index: 9999;
        }
    </style>
    <div class="custom-footer">
        Made with ❤️ by <strong>Abhinav</strong> & <strong>Ajitesh</strong>
    </div>
""", unsafe_allow_html=True)