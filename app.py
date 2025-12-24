import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- STEP 1: GOOGLE VERIFICATION (Must be FIRST) ---
# This plain text helps the Google Bot find your site instantly.
st.write("google-site-verification: UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40")

# This is the hidden meta-tag version for double-security.
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
st.markdown(f'<head><meta name="google-site-verification" content="{GOOGLE_TAG}" /></head>', unsafe_allow_html=True)

# --- STEP 2: APP CONFIG & STYLE ---
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

# --- STEP 3: PUBLIC CONTENT (FOUNDER VISION) ---
# This remains public so the site is never "empty" for the Google bot.
st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Community Sustainability Portal</p></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="founder-box">
    <h3>Founder's Vision</h3>
    <p>"EcoScan Kuwait is a movement to protect our environment by sharing resources. 
    Every swap reduces landfill waste in our beautiful country."</p>
    <p><b>— Founder: Abhilash Babu</b></p>
</div>
""", unsafe_allow_html=True)

# --- STEP 4: LOGIN LOGIC (SIMPLIFIED) ---
# We use a simple system that doesn't require Google Cloud Secrets.
if "user" not in st.session_state: st.session_state.user = None

if not st.session_state.user:
    st.subheader("Member Access")
    phone = st.text_input("Mobile Number")
    pw = st.text_input("Password", type="password")
    
    if st.button("Sign In", type="primary"):
        # This is your special Founder access
        if phone == "90000000" and pw == "founder2025":
            st.session_state.user = {"name": "Abhilash Babu", "phone": phone}
            st.rerun()
        else:
            st.error("Access restricted during Google Verification.")
    
    st.info("Verification in progress. Community Marketplace will open soon.")

else:
    # --- STEP 5: MEMBER AREA (Hidden until Login) ---
    st.success(f"Welcome back, Founder {st.session_state.user['name']}")
    
    if st.button("Log Out"):
        st.session_state.user = None
        st.rerun()
