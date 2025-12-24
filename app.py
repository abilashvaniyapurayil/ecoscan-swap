import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE VERIFICATION ---
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- 2. APP CONFIGURATION ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

# --- 3. PROFESSIONAL BRANDING ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;
    }
    .stButton>button { border-radius: 20px; width: 100%; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# --- 5. SESSION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 6. AUTHENTICATION ---
if not st.session_state.user:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Community Swap Portal</p></div>', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.subheader("Login")
        phone = st.text_input("Mobile Number")
        pw = st.text_input("Password", type="password")
        
        if st.button("Sign In", type="primary"):
            # Founder Login (Change these to your preference)
            if phone == "90000000" and pw == "founder2025":
                st.session_state.user = {"name": "Founder", "phone": phone, "role": "admin", "area": "Kuwait City"}
                st.rerun()
            
            users = load_data(USER_DB)
            user = next((u for u in users if u['phone'] == phone and u['password'] == pw), None)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials.")
        
        if st.button("New? Create Account"):
            st.session_state.view = "signup"
            st.rerun()
            
    else:
        st.subheader("Register")
        new_name = st.text_input("Name")
        new_phone = st.text_input("Phone")
        new_pw = st.text_input("Password", type="password")
        area = st.selectbox("Governorate", ["Asimah", "Hawalli", "Farwaniya", "Ahmadi", "Jahra", "Mubarak"])
        
        if st.button("Join Now"):
            users = load_data(USER_DB)
            users.append({"name": new_name, "phone": new_phone, "password": new_pw, "area": area})
            save_data(USER_DB, users)
            st.success("Success! Please login.")
            st.session_state.view = "login"
            st.rerun()
        if st.button("Back"):
            st.session_state.view = "login"
            st.rerun()

# --- 7. MAIN APP ---
else:
    st.markdown(f'<div class="main-banner"><h1>Welcome to EcoScan</h1><p>Hello, {st.session_state.user["name"]}</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📤 Post", "📱 Feed", "👤 Profile"])
    
    with tab1:
        with st.form("post_form"):
            item = st.text_input("What are you swapping?")
            if st.form_submit_button("Post Listing"):
                items = load_data(ITEM_DB)
                items.append({"name": item, "user": st.session_state.user['name'], "area": st.session_state.user['area']})
                save_
