import streamlit as st
import pandas as pd
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 1. EMAIL SETTINGS (Update these!) ---
# For Gmail, you may need an "App Password" from your Google Account settings.
ADMIN_EMAIL = "your-email@gmail.com" 
EMAIL_PASSWORD = "your-app-password" 

def send_admin_alert(user_name, user_area):
    try:
        msg = MIMEText(f"New User Joined EcoScan Kuwait!\n\nName: {user_name}\nArea: {user_area}\nTime: {datetime.now()}")
        msg['Subject'] = f"🚀 New Member: {user_name}"
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Email alert failed: {e}")

# --- 2. DATA UTILS ---
USER_DB = "users_db.json"
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- 3. UPDATED SIGNUP LOGIC ---
# (Inside your existing Signup view)
if st.session_state.get("view") == "signup":
    st.subheader("Join the Movement")
    s_name = st.text_input("Full Name")
    s_phone = st.text_input("Mobile")
    s_area = st.selectbox("Governorate", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
    s_pw = st.text_input("Password", type="password")
    
    if st.button("Register & Earn 10 Points", type="primary"):
        if s_name and s_phone:
            users = load_data(USER_DB)
            users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pw, "points": 10})
            save_data(USER_DB, users)
            
            # --- TRIGGER EMAIL ALERT ---
            send_admin_alert(s_name, s_area)
            
            st.success("Welcome! Check your email for a (simulated) welcome note.")
            st.session_state.view = "login"
            st.rerun()
