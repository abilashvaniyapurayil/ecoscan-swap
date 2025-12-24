import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE VERIFICATION (Public) ---
# This tag is now at the very top. Google bot will find it here.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- 2. MOBILE APP CONFIG ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

# --- 3. PROFESSIONAL BRANDING (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .stButton>button { border-radius: 20px; width: 100%; height: 3.5em; font-weight: bold; }
    .founder-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #2E7D32; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE (JSON Storage) ---
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

# --- 5. SESSION STATE ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 6. LANDING PAGE & LOGIN (The Public View) ---
if not st.session_state.user:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Reducing Waste. Building Community.</p></div>', unsafe_allow_html=True)
    
    # Founder Message - Always visible on the front page
    st.markdown("""
    <div class="founder-card">
        <h3>Founder's Message</h3>
        <p><i>"EcoScan was born from a simple idea: Kuwait's environment is our shared responsibility. 
        By swapping items instead of discarding them, we reduce landfill waste and strengthen 
        our neighborly bonds. Thank you for being part of this movement."</i></p>
        <small>— EcoScan Founding Team</small>
    </div>
    """, unsafe_allow_html=True)

    # Login/Signup Logic
    if st.session_state.view == "login":
        st.subheader("
