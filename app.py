import streamlit as st
import pandas as pd
import json
import os
from fpdf import FPDF

# 1. BRANDING & CONFIG
st.set_page_config(page_title="EcoScan Kuwait", page_icon="🇰🇼", layout="wide")

USER_DB = "users_db.json"
ITEM_DB = "items_db.json"
FOUNDER_IMAGE = "founder.jpg" # Make sure to upload this exact filename to GitHub
KUWAIT_AREAS = ["Asimah", "Hawalli", "Farwaniya", "Mubarak Al-Kabeer", "Ahmadi", "Jahra"]

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f: 
            try: return json.load(f)
            except: return []
    return []

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

if "user" not in st.session_state: st.session_state.user = None
if "view" not in st.session_state: st.session_state.view = "login"

# --- SIDEBAR: Founder & Account ---
with st.sidebar:
    st.title("🇰🇼 EcoScan Kuwait")
    
    # --- SECTION 1: FOUNDER'S CORNER ---
    st.subheader("👤 Founder's Corner")
    if os.path.exists(FOUNDER_IMAGE):
        st.image(FOUNDER_IMAGE, width=150)
    else:
        st.caption("📷 Photo: Upload 'founder.jpg' to GitHub to see it here.")
    
    st.info("**Message from Abilash:**\nWelcome! I created this platform to help Kuwait transition to a circular economy. Start swapping today!")
    st.divider()

    # --- SECTION 2: ACCOUNT CENTER ---
    if st.session_state.user is None:
        st.markdown("### Quick Login")
        st.button("Continue with Google 🌐", use_container_width=True)
        st.button("Continue with Facebook 🔵", use_container_width=True)
        st.divider()

        if st.session_state.view == "login":
            st.subheader("Login")
            l_phone = st.text_input("Phone Number")
            l_pass = st.text_input("Password", type="password")
            if st.button("Log In", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                u = next((u for u in users if u['phone'] == l_phone and u['password'] == l_pass), None)
                if u:
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Invalid Login")
            
            # Switch to Sign Up
            if st.button("New here? Create Account"):
                st.session_state.view = "signup"
                st.rerun()

        elif st.session_state.view == "signup":
            st.subheader("Register with Phone")
            s_name = st.text_input("Your Full Name")
            s_phone = st.text_input("Mobile Number")
            s_area = st.selectbox("Governorate", KUWAIT_AREAS)
            s_pass = st.text_input("Create Password", type="password")
            if st.button("Register & Join", type="primary", use_container_width=True):
                users = load_json(USER_DB)
                users.append({"name": s_name, "phone": s_phone, "area": s_area, "password": s_pass})
                save_json(USER_DB, users)
                st.success("Success! Please Login.")
                st.session_state.view = "login"
                st.rerun()
            if st.button("Back to Login"):
                st.session_state.view = "login"
                st.rerun()
    else:
        st.success(f"Welcome, {st.session_state.user['name']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

# --- MAIN PAGE ---
st.title("🌱 EcoScan Kuwait")
if st.session_state.user:
    st.write("Community Portal Active.")
else:
    st.warning("Please use the sidebar to Login or Sign Up.")
