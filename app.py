import streamlit as st
from auth import show_welcome_page
from scheduler import schedule_form, view_schedule, delete_schedule, export_schedule_csv
from utils import cleanup
from PIL import Image

# Set up page styling
st.set_page_config(page_title="DMRA Scheduler", layout="centered")
cleanup()

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

# Initialize session state
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# Display login/register screen if not logged in
if st.session_state["user"] is None:
    show_welcome_page()
else:
    # Sidebar with logo and menu
    with st.sidebar:
        image = Image.open("logo.jpeg")
        st.image(image, width=120, use_container_width=False)
        st.markdown(f"**👤 Logged in as:** `{st.session_state['user']}`")

        choice = st.radio("Menu", ["Add Schedule", "View Schedule", "Delete Entry", "Export Schedule", "Logout"])

    # Route choices
    if choice == "Add Schedule":
        schedule_form(st.session_state["user"])
    elif choice == "View Schedule":
        view_schedule(st.session_state["user"])
    elif choice == "Delete Entry":
        delete_schedule(st.session_state["user"])
    elif choice == "Export Schedule":
        if st.session_state.get("role") == "admin":
            export_schedule_csv()
        else:
            st.warning("Only admin users are allowed to export the schedule.")
    elif choice == "Logout":
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.rerun()

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