import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE VERIFICATION ---
# This stays at the top so Google can find it immediately
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- 2. MOBILE APP CONFIG ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

# --- 3. PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .stButton>button { border-radius: 20px; width: 100%; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE (JSON FILES) ---
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

# --- 5. SESSION STATE (Remembers if you are logged in) ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 6. LOGIN / SIGNUP SYSTEM ---
if not st.session_state.user:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Community Swap Portal</p></div>', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.subheader("Login")
        phone = st.text_input("Mobile Number")
        pw = st.text_input("Password", type="password")
        
        if st.button("Sign In", type="primary"):
            users = load_data(USER_DB)
            # Find user by phone and password
            user = next((u for u in users if u['phone'] == phone and u['password'] == pw), None)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid mobile number or password.")
        
        if st.button("New here? Create an Account"):
            st.session_state.view = "signup"
            st.rerun()

    else:
        st.subheader("Create Account")
        new_name = st.text_input("Full Name")
        new_phone = st.text_input("Mobile Number")
        new_pw = st.text_input("Create Password", type="password")
        area = st.selectbox("Governorate", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
        
        if st.button("Register & Join", type="primary"):
            if new_name and new_phone and new_pw:
                users = load_data(USER_DB)
                # Basic check if user already exists
                if any(u['phone'] == new_phone for u in users):
                    st.warning("This mobile number is already registered.")
                else:
                    users.append({"name": new_name, "phone": new_phone, "password": new_pw, "area": area})
                    save_data(USER_DB, users)
                    st.success("Account created! You can now log in.")
                    st.session_state.view = "login"
                    st.rerun()
            else:
                st.error("Please fill in all fields.")
        
        if st.button("Back to Login"):
            st.session_state.view = "login"
            st.rerun()

# --- 7. MAIN APP CONTENT (Only shown after login) ---
else:
    st.markdown(f'<div class="main-banner"><h1>EcoScan Kuwait</h1><p>Welcome, {st.session_state.user["name"]}!</p></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📤 Post", "📱 Feed", "⚙️ Account"])
    
    with tabs[0]:
        st.subheader("Share an Item")
        with st.form("post_item"):
            item_name = st.text_input("What are you sharing?")
            if st.form_submit_button("Post Listing"):
                items = load_data(ITEM_DB)
                items.append({
                    "name": item_name, 
                    "user": st.session_state.user['name'], 
                    "area": st.session_state.user['area'],
                    "date": str(datetime.now().date())
                })
                save_data(ITEM_DB, items)
                st.success("Item posted to the community feed!")
