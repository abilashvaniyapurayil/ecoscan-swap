import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. GOOGLE SEARCH CONSOLE TAG ---
# Keep this at the very top for Google's bots
st.markdown('<head><meta name="google-site-verification" content="UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40" /></head>', unsafe_allow_html=True)

# --- 2. MOBILE APP CONFIG ---
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="centered")

# --- 3. CUSTOM KUWAITI STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F8E9; }
    .main-banner {
        background-color: #2E7D32; color: white;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .stButton>button { border-radius: 20px; width: 100%; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SECRETS CHECK (Prevents the Redacted Error) ---
if "auth" not in st.secrets:
    st.error("⚠️ Setup Required: Please go to Streamlit Cloud Settings and add your [auth] secrets.")
    st.info("I need your Client ID and Client Secret from Google Cloud to function.")
    st.stop()

# --- 5. SOCIAL LOGIN LOGIC ---
if not st.user.is_logged_in:
    st.markdown('<div class="main-banner"><h1>🇰🇼 EcoScan Kuwait</h1><p>The Circular Economy for Kuwait</p></div>', unsafe_allow_html=True)
    st.subheader("Join the community")
    
    if st.button("Continue with Google", type="primary"):
        st.login() # This triggers the Google handshake
    st.stop() 

# --- 6. MAIN APP INTERFACE (Only shown after login) ---
st.markdown(f'<div class="main-banner"><h1>EcoScan Kuwait</h1><p>Hello, {st.user.name}!</p></div>', unsafe_allow_html=True)

menu = ["Marketplace Feed", "Post an Item", "My Account"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Post an Item":
    st.subheader("What are you sharing today?")
    with st.form("post_form"):
        item = st.text_input("Item Name")
        area = st.selectbox("Area", ["Hawalli", "Salmiya", "Kuwait City", "Jahra"])
        if st.form_submit_button("Post to Marketplace"):
            st.success(f"Listing created for {item}!")

elif choice == "Marketplace Feed":
    st.subheader("Live Listings in Kuwait")
    st.info("Searching for items near you...")

elif choice == "My Account":
    st.write(f"**Verified Email:** {st.user.email}")
    if st.button("Log Out"):
        st.logout()
