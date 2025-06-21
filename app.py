import streamlit as st
from auth import login
from scheduler import schedule_form, view_schedule
from utils import cleanup

st.title("📘 Professor Scheduler")

# Clean up old entries
cleanup()

if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    login()
else:
    st.sidebar.success(f"Logged in as {st.session_state['user']}")
    choice = st.sidebar.radio("Menu", ["Add Schedule", "View Schedule", "Logout"])

    if choice == "Add Schedule":
        schedule_form(st.session_state["user"])
    elif choice == "View Schedule":
        view_schedule(st.session_state["user"])
    elif choice == "Logout":
        st.session_state["user"] = None
        st.experimental_rerun()