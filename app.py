import streamlit as st
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. GLOBAL BRANDING & CONFIG
st.set_page_config(
    page_title="EcoScan Kuwait", 
    page_icon="🇰🇼", 
    layout="wide"
)

# --- Constants & Database ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
FOUNDER_IMAGE = "founder.jpg" # Ensure this matches your GitHub filename exactly
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f: 
            try: return json.load(f)
            except: return []
    return []

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# --- Session State Management ---
if "user" not in st.session_state:
    st.session_state.user = None
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- SIDEBAR: Brand & Founder's Corner ---
with st.sidebar:
    st.title("🇰🇼 EcoScan Kuwait")
    
    # Founder Section
    st.divider()
    if os.path.exists(FOUNDER_IMAGE):
        st.image(FOUNDER_IMAGE, width=150, caption="Founder & Developer")
    else:
        st.info("Founder Photo: Uploading... (Ensure 'founder.jpg' is in GitHub)")
    
    st.markdown("""
    **Founder's Message** Hi! I'm Abilash. I built **EcoScan Kuwait** to help our community swap items and reduce waste across the nation. Let's make Kuwait greener!
    """)
    st.divider()

    # Authentication UI
    if st.session_state.user is None:
        st.subheader("Account Access")
        # Social Login UI (Buttons only for now)
        st.button("Continue with Google 🌐", use_container_width=True)
        st.button("Continue with Facebook 🔵", use_container_width=True)
        st.divider()
