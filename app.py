import streamlit as st
import pandas as pd
import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components

# --- 1. SEARCH & SOCIAL VERIFICATION ---
# Your specific Google HTML Tag integrated here
GOOGLE_TAG = "UbGI9p25Kivjr9u465NRYSpRTy4euChN-XFrwiy3r40"
META_TAG = "YOUR_META_VERIFICATION_CODE_HERE" # Replace when you get this from Meta

# Injecting the verification tags into the app header
components.html(
    f"""
    <html>
        <head>
            <meta name="google-site-verification" content="{GOOGLE_TAG}" />
            <meta name="facebook-domain-verification" content="{META_TAG}" />
        </head>
    </html>
    """,
    height=0,
)

# --- 2. MOBILE-FIRST APP CONFIG ---
st.set_page_config(
    page_title="EcoScan Kuwait",
    page_icon="🇰🇼",
    layout="centered"
)

# --- 3. PROFESSIONAL MOBILE STYLING (CSS) ---
st.markdown("""
    <style>
    /* Custom Theme Colors */
    .stApp { background-color: #F1F8E9; }
    
    /* Branded Top Banner */
    .main-banner {
        background-color: #2E7D32;
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Professional Mobile Buttons */
    .stButton>button {
        border-radius: 25px;
        width: 100%;
        height: 3.5em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        border: none;
    }

    /* Tabs Styling */
    div.stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ENGINE (JSON) ---
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

# --- 5. SESSION LOGIC ---
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- 6. MAIN APP INTERFACE ---
if st.session_state.user:
    # Check if Admin
    is_admin = st.session_state.user.get("role") == "admin"
    
    # Branded Header
    st.markdown('<div class="main-banner"><h1>EcoScan Kuwait</h1><p>The Future of Community Swapping</p></div>', unsafe_allow_html=True)
    
    # Navigation Tabs
    tabs = st.tabs(["📤 Post", "📱 Feed", "🏆 Top", "⚖️ Legal"])

    # TAB: POST ITEM
    with tabs[0]:
        st.subheader("Earn Eco-Points")
        with st.form("post_item", clear_on_submit=True):
            name = st.text_input("What are you giving away?")
            cat = st.selectbox("Category", ["Electronics", "Furniture", "Books", "Clothes", "Other"])
            desc = st.text_area("Item Details")
            if st.form_submit_button("Publish Nationally (+10 Points)"):
                if name:
                    items = load_data(ITEM_DB)
                    items.append({
                        "id": str(datetime.now().timestamp()),
                        "name": name, "cat": cat, "desc": desc,
                        "user": st.session_state.user['name'],
                        "area": st.session_state.user['area']
                    })
                    save_data(ITEM_DB, items)
                    
                    # Add Points to User Account
                    users = load_data(USER_DB)
                    for u in users:
                        if u['phone'] == st.session_state.user['phone']:
                            u['points'] =
