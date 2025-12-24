import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

# --- Database Setup ---
USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
FOUNDER_IMAGE = "founder.jpeg" # Verified as working in your repository
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f: 
            try: return json.load(f)
            except: return []
    return []

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

# Initialize Session States
if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- SIDEBAR: Brand & Account ---
with st.sidebar:
    st.header("🇰🇼 EcoScan Kuwait")
    
    # Founder's Corner (Verified Working)
    st.subheader("👤 Founder's Corner")
    if os.path.exists(FOUNDER_IMAGE):
        st.image(FOUNDER_IMAGE, use_container_width=True)
        st.info("**Abilash's Message:** Let's build a greener Kuwait together through community swapping!")
    
    st.divider()

    # Account Management Logic
    if st.session_state.user is None:
        if st.session_state.view == "login":
            st.markdown("### 🔑 Login")
            l_phone = st.text_input("Phone Number")
            l_pass = st.text_input("Password", type="password")
            if st.button("Log In", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                u = next((u for u in users if u['phone'] == l_phone and u['password'] == l_pass), None)
                if u:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Invalid Login")
            
            if st.button("New here? Create Account"):
                st.session_state.view = "signup"
                st.rerun()

        elif st.session_state.view == "signup":
            st.markdown("### 📝 Register")
            s_name = st.text_input("Full Name")
            s_phone = st.text_input("Mobile Number")
            s_area = st.selectbox("Governorate", KUWAIT_AREAS)
            s_pass = st.text_input("Password", type="password")
            if st.button("Register Now", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pass})
