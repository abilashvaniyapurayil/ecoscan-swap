import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE VERIFICATION ---
# This matches the code Google gave you. It must be at the very top.
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

# --- 4. GOOGLE SOCIAL LOGIN LOGIC ---
# This uses the built-in st.user feature which reads your secrets.toml
if not st.user.is_logged_in:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>Kuwait\'s Sustainability Community</p></div>', unsafe_allow_html=True)
    st.subheader("Welcome! Please Sign In")
    
    if st.button("Continue with Google", type="primary"):
        st.login() # This looks at your secrets.toml automatically
    
    st.info("By signing in, you help make Kuwait greener.")
    st.stop() 

# --- 5. MAIN APP (Only visible if logged in) ---
st.markdown(f'<div class="main-banner"><h1>EcoScan Kuwait</h1><p>Welcome, {st.user.name}!</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["📤 Post Item", "📱 Feed", "⚙️ Account"])

with tabs[0]:
    st.subheader("List an item to swap")
    item = st.text_input("What are you sharing?")
    if st.button("Post Now"):
        st.success(f"Successfully listed {item}!")

with tabs[1]:
    st.subheader("Community Listings")
    st.write("No items found in your area yet.")

with tabs[2]:
    st.write(f"Logged in as: {st.user.email}")
    if st.button("Log Out"):
        st.logout()
