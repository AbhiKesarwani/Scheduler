import streamlit as st
import pandas as pd
from PIL import Image
import os

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

USER_DB = "users.xlsx"

def init_user_file():
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=["Username", "Password", "Role"])
        df.to_excel(USER_DB, index=False)

def show_welcome_page():
    init_user_file()
    st.markdown("<h1 style='text-align: center; color: #003366;'>👋 Welcome to DMRA Scheduler</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        image = Image.open("logo.jpeg")  # make sure the image file is named logo.jpeg
        st.image(image, width=250)

    st.markdown("<h4 style='text-align: center;'>Log in or register to continue</h4>", unsafe_allow_html=True)

    auth_option = st.radio("Choose Option", ["Login", "Register"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_option == "Register":
        if st.button("Create Account"):
            df = pd.read_excel(USER_DB)
            if username in df["Username"].values:
                st.error("🚫 Username already exists. Choose a different one.")
            elif username and password:
                new_user = pd.DataFrame([[username, password, "user"]], columns=["Username", "Password", "Role"])
                df = pd.concat([df, new_user], ignore_index=True)
                df.to_excel(USER_DB, index=False)
                st.success("🎉 Registration successful! You can now log in.")
            else:
                st.warning("Please enter both username and password.")
    else:
        if st.button("Login"):
            df = pd.read_excel(USER_DB)
            match = df[(df["Username"] == username) & (df["Password"] == password)]
            if not match.empty:
                st.session_state["user"] = username
                st.session_state["role"] = match.iloc[0]["Role"]
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("Incorrect username or password.")

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