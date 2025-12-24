import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE VERIFICATION (MUST BE FIRST) ---
# This tag must be outside any 'if' statements so Google can find it.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- 2. APP CONFIGURATION ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

# --- 3. BRANDING & STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .founder-message {
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; margin-bottom: 20px; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE ---
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

# --- 5. LOGIN SESSION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 6. PUBLIC LANDING PAGE (Founder Messages) ---
if not st.session_state.user:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Kuwait\'s Community Sustainability Hub</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="founder-message">
        <h3>Founder's Vision</h3>
        "EcoScan was built to protect Kuwait's beauty. By sharing instead of discarding, 
        we reduce waste in our landfills and build a stronger, kinder community."
        <br><br><b>— Abhilash Babu</b>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🌍 About the Project", expanded=True):
        st.write("EcoScan is a platform for swapping items within Kuwait neighborhoods. "
                 "Join us to earn Eco-Points and make our environment cleaner.")

    st.divider()

    # Simple ID & Password Login (No Google OAuth needed)
    if st.session_state.view == "login":
        st.subheader("Login")
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
                st.error("Invalid credentials.")
        
        if st.button("New here? Create Account"):
            st.session_state.view = "signup"
            st.rerun()
    else:
        st.subheader("Register")
        # (Signup inputs follow the same logic as previous version)
        if st.button("Back to Login"):
            st.session_state.view = "login"
            st.rerun()

# --- 7. PRIVATE DASHBOARD (Visible After Login) ---
else:
    st.markdown(f'<div class="main-banner"><h1>Welcome back, {st.session_state.user["name"]}</h1></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📤 Post", "📱 Feed", "👤 Profile"])
    
    with tabs[1]:
        st.subheader("Community Marketplace")
        # Search Bar for Items
        query = st.text_input("Search for items in Kuwait...")
        # (Listing logic goes here)

    with tabs[2]:
        if st.button("Log Out"):
            st.session_state.user = None
            st.rerun()
