import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. THE "PUBLIC" HEADER (Always visible to Google & Visitors) ---
# This remains outside any 'if' statements so Google can always find it.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- 2. APP CONFIG & STYLE ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .founder-box {
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA STORAGE ENGINE ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- 4. PERMANENT PUBLIC CONTENT (Founder Details) ---
# This part is seen by Google and users before they log in.
st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Community Sustainability Portal</p></div>', unsafe_allow_html=True)

st.markdown("""
<div class="founder-box">
    <h3>Our Vision</h3>
    <p><i>"EcoScan Kuwait is more than an app; it is a movement to protect our environment 
    by sharing resources. Every swap reduces landfill waste in our beautiful country."</i></p>
    <p><b>— Founder: Abhilash Babu</b></p>
</div>
""", unsafe_allow_html=True)

# --- 5. AUTHENTICATION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

if not st.session_state.user:
    # --- LOGIN / SIGNUP SECTION ---
    if st.session_state.view == "login":
        st.subheader("Member Login")
        phone = st.text_input("Mobile Number")
        pw = st.text_input("Password", type="password")
        
        if st.button("Sign In", type="primary"):
            # Founder Admin Login
            if phone == "90000000" and pw == "founder2025":
                st.session_state.user = {"name": "Abhilash Babu", "phone": phone, "role": "admin", "area": "Kuwait City"}
                st.rerun()
            
            users = load_data(USER_DB)
            user = next((u for u in users if u['phone'] == phone and u['password'] == pw), None)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        
        if st.button("No account? Register here"):
            st.session_state.view = "signup"
            st.rerun()
    else:
        st.subheader("Create Account")
        name = st.text_input("Name")
        new_phone = st.text_input("Phone")
        new_pw = st.text_input("Password", type="password")
        if st.button("Join Community"):
            users = load_data(USER_DB)
            users.append({"name": name, "phone": new_phone, "password": new_pw, "area": "Kuwait"})
            save_data(USER_DB, users)
            st.success("Registered! Please login.")
            st.session_state.view = "login"
            st.rerun()
        if st.button("Back"):
            st.session_state.view = "login"
            st.rerun()

else:
    # --- 6. SECURE APP CONTENT (Only for logged-in users) ---
    st.success(f"Logged in as {st.session_state.user['name']}")
    
    tabs = st.tabs(["📤 Post Item", "📱 Community Feed", "⚙️ Account"])
    
    with tabs[0]:
        st.subheader("Share something with neighbors")
        item = st.text_input("What are you sharing?")
        if st.button("Post Now"):
            items = load_data(ITEM_DB)
            items.append({"name": item, "user": st.session_state.user['name']})
            save_data(ITEM_DB, items)
            st.success("Listing added!")

    with tabs[1]:
        st.subheader("Available in Kuwait")
        all_items = load_data(ITEM_DB)
        for i in reversed(all_items):
            st.info(f"{i['name']} (Shared by {i['user']})")

    with tabs[2]:
        if st.button("Log Out"):
            st.session_state.user = None
            st.rerun()
